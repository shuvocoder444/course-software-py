from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

# আপনার অ্যাকাউন্টস অ্যাপ থেকে কাস্টম সিকিউরিটি ও লেআউট মিক্সিন ইম্পোর্ট
from apps.account.views import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin

from .forms import StudentForm

# বর্তমান অ্যাপের মডেল এবং ফর্ম ইম্পোর্ট
from .models import Student

# ==============================================================================
#  ৬. স্টুডেন্ট ম্যানেজমেন্ট CRUD ভিউ (CBV - Admin Only) - FULL FIXED
# ==============================================================================

from django.views.generic import DetailView
# আপনার প্রজেক্টের মিক্সিন ইম্পোর্ট করুন
# from your_apps.mixins import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin

# ১. STUDENT LIST VIEW (With Live Filters)
class StudentListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student.html'
    ordering = ['-id']

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
        # ফিল্টার ড্রপডাউনে দেখানোর জন্য সব কোর্স ও ব্যাচ পাঠানো হচ্ছে
        from apps.courses.models import Batch, Course
        context['courses'] = Course.objects.all()
        context['batches'] = Batch.objects.all()
        return context


# ২. STUDENT APPROVE VIEW (Approve বাটনের জন্য)
class StudentApproveView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        student = get_object_or_404(Student, pk=pk)

        # স্ট্যাটাস পরিবর্তন করে 'active' বা 'approved' করা (আপনার মডেল অনুযায়ী)
        student.status = 'active'
        student.save()

        messages.success(request, f"{student.name}-এর আবেদন সফলভাবে অ্যাপ্রুভ করা হয়েছে।")
        return redirect('student_list') # আপনার স্টুডেন্ট লিস্টের URL name এখানে দিন


# ৩. STUDENT PRINT VIEW (Print বাটনের জন্য)
class StudentPrintView(LoginRequiredMixin, AdminRoleRequiredMixin, DetailView):
    model = Student
    template_name = 'student_print.html' # প্রিন্ট করার জন্য একটি আলাদা সিম্পল HTML টেমপ্লেট
    context_object_name = 'student'


# ২. CREATE STUDENT VIEW
class StudentCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'  # সরাসরি templates ফোল্ডার থেকে লোড হবে
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        # ফর্ম সেভ করার আগে অবজেক্টটি মেমরিতে হোল্ড করা হলো (ডাটাবেজে এখনই সেভ হবে না)
        student = form.save(commit=False)

        # ১. অটোমেটিক স্টুডেন্ট আইডি জেনারেশন লজিক (যেমন: STU-2026-0001)
        current_year = datetime.now().year # ২০২৬ বা কারেন্ট ইয়ার নিবে
        last_student = Student.objects.order_by('-id').first()

        if last_student:
            next_id = last_student.id + 1
        else:
            next_id = 1

        student.student_id = f"STU-{current_year}-{next_id:04d}" # আউটপুট: STU-2026-0001

        # ২. অটোমেটিক সেশন সেট করা
        next_year = current_year + 1
        student.session = f"{current_year}-{next_year}" # আউটপুট: 2026-2027

        # ৩. স্ট্যাটাস মডেলে ডিফল্ট 'pending' দেওয়া আছে, তাও নিশ্চিত করার জন্য:
        student.status = 'pending'

        # ডেটাবেজে ফাইনাল সেভ
        student.save()

        messages.success(self.request, f"Student {student.name} created successfully with ID: {student.student_id}")
        return super().form_valid(form)


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
