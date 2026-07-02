from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model  # <--- এটি যুক্ত করুন
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

# কাস্টম ইউজার মডেল একটি ভেরিয়েবলে নেওয়া হলো
User = get_user_model()  # <--- এটি যুক্ত করুন

# আপনার অ্যাকাউন্টস অ্যাপ থেকে কাস্টম সিকিউরিটি ও লেআউট মিক্সিন ইম্পোর্ট
# ... বাকি কোড অপরিবর্তিত থাকবে ...
# ==============================================================================
#  ৬. স্টুডেন্ট ম্যানেজমেন্ট CRUD ভিউ (CBV - Admin Only) - FULL FIXED
# ==============================================================================
from django.views.generic import DetailView

from apps.account.views import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin

from .forms import StudentForm
from .models import Student


# আপনার প্রজেক্টের মিক্সিন ইম্পোর্ট করুন
# from your_apps.mixins import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin
# ১. STUDENT LIST VIEW (With Live Filters & Pagination)
class StudentListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student.html'
    ordering = ['-id']
    paginate_by = 10  # 👑 প্রতি পেজে কয়টি রেকর্ড দেখাতে চান তা এখানে সেট করুন

    def get_queryset(self):
        queryset = super().get_queryset()

        # ফ্রন্টএন্ড ফিল্টার থেকে ডেটা নেওয়া
        search_query = self.request.GET.get('search', '')
        course_filter = self.request.GET.get('course', '')
        batch_filter = self.request.GET.get('batch', '')

        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | queryset.filter(student_id__icontains=search_query) | queryset.filter(phone__icontains=search_query)

        if course_filter:
            queryset = queryset.filter(course_id=course_filter)

        if batch_filter:
            queryset = queryset.filter(batch_id=batch_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.courses.models import Batch, Course
        context['courses'] = Course.objects.all()
        context['batches'] = Batch.objects.all()
        return context

from .models import Student

# আপনার কাস্টম মিক্সিনগুলো ইমপোর্ট করে নিয়েন (যেমন: LoginRequiredMixin, AdminRoleRequiredMixin)

# ৩. STUDENT PRINT VIEW
class StudentPrintView(LoginRequiredMixin, AdminRoleRequiredMixin, DetailView):
    model = Student
    template_name = 'print.html' # আপনার ফাইলের নাম অনুযায়ী 'print.html' করা হলো
    context_object_name = 'student'

# ৪. STUDENT APPROVE VIEW (এই ভিউটি মিসিং ছিল)
class StudentApproveView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        student = get_object_or_404(Student, pk=pk)
        student.status = 'approved' # অথবা আপনার মডেলে যেভাবে 'active'/'approved' সেট করা আছে
        student.save()
        messages.success(request, f"{student.name}-এর অ্যাডমিশন অ্যাপ্রুভ করা হয়েছে।")
        return redirect('student_list') # আপনার স্টুডেন্ট লিস্টের URL name এখানে দিন




# ২. CREATE STUDENT VIEW (Username & Password = Phone Number)
class StudentCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        # ১. ফর্মের ডেটা মেমরিতে হোল্ড করা (ফর্ম থেকে student_id সহ সব ডেটা আসবে)
        student = form.save(commit=False)

        # ২. অটোমেটিক সেশন সেট করা
        current_year = datetime.now().year
        next_year = current_year + 1
        student.session = f"{current_year}-{next_year}"

        # ৩. স্ট্যাটাস নিশ্চিত করা
        student.status = 'pending'

        # ==============================================================================
        # ৪. স্বয়ংক্রিয়ভাবে ইউজার অ্যাকাউন্ট তৈরি করার লজিক (Username & Password = Phone)
        # ==============================================================================
        student_phone = form.cleaned_data.get('phone')
        student_email = form.cleaned_data.get('email')
        student_name = form.cleaned_data.get('name')

        if student_phone:
            # চেক করা হচ্ছে এই ফোন নাম্বার দিয়ে অলরেডি কোনো অ্যাকাউন্ট আছে কি না
            if not User.objects.filter(username=student_phone).exists():
                # নতুন ইউজার তৈরি (ইউজারনেম এবং পাসওয়ার্ড দুটোই ফোন নাম্বার)
                user = User.objects.create_user(
                    username=student_phone,  # ডিফল্ট ইউজারনেম = ফোন নাম্বার
                    password=student_phone,  # ডিফল্ট পাসওয়ার্ড = ফোন নাম্বার
                    email=student_email if student_email else '', # ইমেইল থাকলে সেভ হবে, না থাকলে খালি থাকবে
                    first_name=student_name
                )

                # আপনার Student মডেলে যদি User-এর সাথে সম্পর্ক (user field) থাকে, তবে লিংক করে দিন:
                # student.user = user
            else:
                messages.warning(self.request, f"এই ফোন নাম্বার ({student_phone}) দিয়ে ইতিমধ্যে একটি অ্যাকাউন্ট তৈরি করা আছে!")
        else:
            messages.error(self.request, "স্টুডেন্টের মোবাইল নাম্বার পাওয়া যায়নি! অ্যাকাউন্ট তৈরি করা সম্ভব হয়নি।")
            return self.form_invalid(form)
        # ==============================================================================

        # ৫. ডেটাবেজে ফাইনাল স্টুডেন্ট সেভ
        student.save()

        messages.success(self.request, f"Student {student.name} created successfully! ID: {student.student_id}. User account created with Phone Number.")
        return redirect(self.success_url)


# ৩. EDIT / UPDATE STUDENT VIEW
class StudentEditView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'  # সরাসরি templates ফোল্ডার থেকে লোড হবে
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, "Student profile updated successfully!")
        return super().form_valid(form)


# ৪. DELETE STUDENT VIEW
class StudentDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk):
        student_instance = get_object_or_404(Student, pk=pk)
        student_name = student_instance.name
        student_instance.delete()
        messages.success(request, f"Student '{student_name}' record deleted successfully!")
        return redirect('student_list')

    def get(self, request, pk):
        # সিকিউরিটির জন্য GET রিকোয়েস্ট আসলেও পোস্ট মেথডেই রিডাইরেক্ট করা হলো
        return self.post(request, pk)



from django.http import JsonResponse

from apps.courses.models import Batch  # আপনার অ্যাপ স্ট্রাকচার অনুযায়ী পাথ


# ৫. AJAX API VIEW (কোর্সের আইডি অনুযায়ী ব্যাচ লোড করার জন্য)
class LoadBatchesView(View):
    def get(self, request):
        course_id = request.GET.get('course_id')
        # কোর্স আইডি অনুযায়ী ফিল্টার করে শুধু id এবং batch_number পাঠানো হচ্ছে
        batches = Batch.objects.filter(course_id=course_id).values('id', 'batch_number')
        return JsonResponse(list(batches), safe=False)
