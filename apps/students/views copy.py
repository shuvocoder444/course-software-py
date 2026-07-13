from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from apps.account.views import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin
from apps.courses.models import Batch  # আপনার অ্যাপ স্ট্রাকচার অনুযায়ী পাথ
from apps.setting.models import AttendenceSetting
from apps.setting.utils import send_sms

from .forms import StudentForm
from .models import Student

# কাস্টম ইউজার মডেল একটি ভেরিয়েবলে নেওয়া হলো
User = get_user_model()


# ==============================================================================
#  ১. STUDENT LIST VIEW (With Live Filters & Pagination)
# ==============================================================================
class StudentListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student.html'
    ordering = ['-id']
    paginate_by = 10  # প্রতি পেজে ১০টি রেকর্ড দেখাবে

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
        from apps.courses.models import Course
        context['courses'] = Course.objects.all()
        context['batches'] = Batch.objects.all()
        return context


# ==============================================================================
#  ২. STUDENT PRINT VIEW
# ==============================================================================
class StudentPrintView(LoginRequiredMixin, AdminRoleRequiredMixin, DetailView):
    model = Student
    template_name = 'print.html'
    context_object_name = 'student'


# ==============================================================================
#  ৩. STUDENT APPROVE VIEW
# ==============================================================================
class StudentApproveView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        student = get_object_or_404(Student, pk=pk)
        student.status = 'approved'
        student.save()
        messages.success(request, f"{student.name}-এর অ্যাডমিশন অ্যাপ্রুভ করা হয়েছে।")
        return redirect('student_list')


# ==============================================================================
#  ৪. CREATE STUDENT VIEW (Username & Password = Phone Number)
# ==============================================================================
# class StudentCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
#     model = Student
#     form_class = StudentForm
#     template_name = 'student_form.html'
#     success_url = reverse_lazy('student_list')

#     def form_valid(self, form):
#         # ১. ফর্মের ডেটা মেমরিতে হোল্ড করা
#         student = form.save(commit=False)

#         # ২. অটোমেটিক সেশন সেট করা
#         current_year = datetime.now().year
#         next_year = current_year + 1
#         student.session = f"{current_year}-{next_year}"

#         # ৩. স্ট্যাটাস নিশ্চিত করা
#         student.status = 'pending'

#         # ৪. স্বয়ংক্রিয়ভাবে ইউজার অ্যাকাউন্ট তৈরি এবং লিঙ্ক করার লজিক
#         student_phone = form.cleaned_data.get('phone')
#         student_email = form.cleaned_data.get('email')
#         student_name = form.cleaned_data.get('name')

#         if student_phone:
#             # আগে থেকে এই ফোন নাম্বার দিয়ে কোনো অ্যাকাউন্ট আছে কিনা চেক করা হচ্ছে
#             user_instance = User.objects.filter(username=student_phone).first()

#             if not user_instance:
#                 # নতুন ইউজার তৈরি (ইউজারনেম এবং পাসওয়ার্ড দুটোই ফোন নাম্বার)
#                 user_instance = User.objects.create_user(
#                     username=student_phone,
#                     password=student_phone,
#                     email=student_email if student_email else '',
#                     first_name=student_name
#                 )
#             else:
#                 messages.warning(self.request, f"এই ফোন নাম্বার ({student_phone}) দিয়ে ইতিমধ্যে একটি অ্যাকাউন্ট তৈরি করা আছে! সেটিই এই স্টুডেন্টের সাথে লিঙ্ক করা হলো।")

#             # 👑 ফিক্সড লজিক: তৈরি হওয়া বা আগের ইউজার অ্যাকাউন্টটি স্টুডেন্টের ওয়ান-টু-ওয়ান ফিল্ডে লিঙ্ক করা হলো
#             student.account = user_instance
#         else:
#             messages.error(self.request, "স্টুডেন্টের মোবাইল নাম্বার পাওয়া যায়নি! অ্যাকাউন্ট তৈরি করা সম্ভব হয়নি।")
#             return self.form_invalid(form)

#         # ৫. ডেটাবেজে ফাইনাল স্টুডেন্ট সেভ
#         student.save()

#         messages.success(self.request, f"Student {student.name} created successfully! ID: {student.student_id}. User account created with Phone Number.")
#         return redirect(self.success_url)


class StudentCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        # ১. ফর্মের ডেটা মেমরিতে হোল্ড করা
        student = form.save(commit=False)

        # ২. অটোমেটিক সেশন সেট করা
        current_year = datetime.now().year
        next_year = current_year + 1
        student.session = f"{current_year}-{next_year}"

        # ৩. স্ট্যাটাস নিশ্চিত করা
        student.status = 'pending'

        # ৪. স্বয়ংক্রিয়ভাবে ইউজার অ্যাকাউন্ট তৈরি এবং লিঙ্ক করার লজিক
        student_phone = form.cleaned_data.get('phone')
        student_email = form.cleaned_data.get('email')
        student_name = form.cleaned_data.get('name')

        if student_phone:
            # আগে থেকে এই ফোন নাম্বার দিয়ে কোনো অ্যাকাউন্ট আছে কিনা চেক করা হচ্ছে
            user_instance = User.objects.filter(username=student_phone).first()

            if not user_instance:
                # নতুন ইউজার তৈরি (ইউজারনেম এবং পাসওয়ার্ড দুটোই ফোন নাম্বার)
                user_instance = User.objects.create_user(
                    username=student_phone,
                    password=student_phone,
                    email=student_email if student_email else '',
                    first_name=student_name
                )
            else:
                messages.warning(self.request, f"এই ফোন নাম্বার ({student_phone}) দিয়ে ইতিমধ্যে একটি অ্যাকাউন্ট তৈরি করা আছে! সেটিই এই স্টুডেন্টের সাথে লিঙ্ক করা হলো।")

            # তৈরি হওয়া বা আগের ইউজার অ্যাকাউন্টটি স্টুডেন্টের ওয়ান-টু-ওয়ান ফিল্ডে লিঙ্ক করা হলো
            student.account = user_instance
        else:
            messages.error(self.request, "স্টুডেন্টের মোবাইল নাম্বার পাওয়া যায়নি! অ্যাকাউন্ট তৈরি করা সম্ভব হয়নি।")
            return self.form_invalid(form)

        # ৫. ডেটাবেজে ফাইনাল স্টুডেন্ট সেভ
        student.save()

        # ৬. ডাটাবেজ থেকে বাংলা এসএমএস টেমপ্লেট নিয়ে লাইভ এসএমএস পাঠানো এবং স্ট্যাটাস ট্র্যাক করা
        sms_sent = False
        sms_error_reason = "Unknown Error"

        try:
            settings_instance = AttendenceSetting.objects.first()
            if settings_instance and settings_instance.reg_sms:
                # ডাটাবেজের বাংলা মেসেজ থেকে শর্টকোডগুলো রিপ্লেস করা হচ্ছে
                custom_message = settings_instance.reg_sms
                custom_message = custom_message.replace("[name]", student.name)
                custom_message = custom_message.replace("[phone]", student_phone)

                # JBD IT SMS Gateway এর মাধ্যমে এসএমএস সেন্ড এবং রেসপন্স রিসিভ
                is_success, api_message = send_sms(student_phone, custom_message)
                if is_success:
                    sms_sent = True
                else:
                    sms_error_reason = api_message
            else:
                sms_error_reason = "SMS Settings অথবা টেমপ্লেট ডাটাবেজে কনফিগার করা নেই।"
        except Exception as e:
            sms_error_reason = str(e)

        # ৭. ডাইনামিক স্ক্রিন মেসেজ (মেসেজ সফলভাবে গেলে একরকম, ফেইল করলে অন্যরকম সতর্কবার্তা দেখাবে)
        if sms_sent:
            messages.success(self.request, f"স্টুডেন্ট {student.name} সফলভাবে তৈরি হয়েছে! আইডি: {student.student_id} এবং স্বাগতম এসএমএস পাঠানো হয়েছে।")
        else:
            messages.success(self.request, f"স্টুডেন্ট {student.name} তৈরি হয়েছে (আইডি: {student.student_id})।")
            messages.error(self.request, f"⚠️ কিন্তু ওয়েলকাম এসএমএস পাঠানো যায়নি! কারণ: {sms_error_reason}")

        return redirect(self.success_url)


# ==============================================================================
#  ৫. EDIT / UPDATE STUDENT VIEW
# ==============================================================================
class StudentEditView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, "Student profile updated successfully!")
        return super().form_valid(form)


# ==============================================================================
#  ৬. DELETE STUDENT VIEW
# ==============================================================================
class StudentDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk):
        student_instance = get_object_or_404(Student, pk=pk)
        student_name = student_instance.name
        student_instance.delete()
        messages.success(request, f"Student '{student_name}' record deleted successfully!")
        return redirect('student_list')

    def get(self, request, pk):
        return self.post(request, pk)


# ==============================================================================
#  ৭. AJAX API VIEW (কোর্সের আইডি অনুযায়ী ব্যাচ লোড করার জন্য)
# ==============================================================================
class LoadBatchesView(View):
    def get(self, request):
        course_id = request.GET.get('course_id')
        # কোর্স আইডি অনুযায়ী ফিল্টার করে শুধু id এবং batch_number পাঠানো হচ্ছে
        batches = Batch.objects.filter(course_id=course_id).values('id', 'batch_number')
        return JsonResponse(list(batches), safe=False)







from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.courses.models import Course  # কোর্স মডেল ইম্পোর্ট করা হলো
from apps.students.models import Student  # স্টুডেন্ট মডেল ইম্পোর্ট করা হলো


@login_required
def student_dashboard(request):
    # ১. লগইন করা ইউজারের সাথে যুক্ত স্টুডেন্ট প্রোফাইলটি খোঁজা হচ্ছে
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = None

    # ২. ডাটাবেজ থেকে সব কোর্স কুয়েরি করে আনা হচ্ছে (যাতে নিচে শো করে)
    # আপনি চাইলে এখানে [:4] দিয়ে সর্বোচ্চ ৪টি কোর্স দেখাতে পারেন
    best_courses = Course.objects.all()

    # ৩. কনটেক্সটের মাধ্যমে ডাটা HTML-এ পাঠানো হচ্ছে
    context = {
        "student": student,
        "best_courses": best_courses,
    }

    # আপনার বর্তমান টেমপ্লেট পাথ অনুযায়ী রেন্ডার করা হলো
    return render(request, "student.html", context)
