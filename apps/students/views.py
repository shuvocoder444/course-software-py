from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
# apps/students/views.py ফাইলের ৭৭ নম্বর লাইনে যান এবং এটি লিখুন:
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
#  ৩. STUDENT APPROVE VIEW (WITH SMS LOGGING)
# ==============================================================================
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# 🎯 আপনার সঠিক পাথ অনুযায়ী প্রয়োজনীয় মডেল ও ফাংশনগুলো ইম্পোর্ট করে নিন
from apps.students.models import Student
from apps.setting.models import SMSLog  # SMSLog ইম্পোর্ট করা হলো


class StudentApproveView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        student = get_object_or_404(Student, pk=pk)

        # স্ট্যাটাস পরিবর্তন
        student.status = 'approved'
        student.save()

        # ডাইনামিক এসএমএস লজিক
        sms_sent = False
        sms_error_reason = "Unknown Error"
        custom_message = ""

        try:
            # সেটিংস অ্যাপের মডেল থেকে ডাটা লোড করা হচ্ছে
            settings_instance = AttendenceSetting.objects.first()

            if settings_instance and settings_instance.approve_sms:
                custom_message = settings_instance.approve_sms
            else:
                # কোনো কারণে সেটিংসে মেসেজ না থাকলে ব্যাকআপ ডিফল্ট মেসেজ
                custom_message = f"প্রিয় {student.name}, আপনার ভর্তি সফলভাবে অ্যাপ্রুভ করা হয়েছে। আইডি: {student.student_id}।"

            # সেটিংসের টেক্সট থেকে শর্টকোড ডাইনামিকালি রিপ্লেস করা হচ্ছে
            custom_message = custom_message.replace("[name]", student.name)
            custom_message = custom_message.replace("[id]", str(student.student_id))

            # JBD IT SMS Gateway কল
            if student.phone:
                is_success, api_message = send_sms(student.phone, custom_message)
                if is_success:
                    sms_sent = True

                    # 🎯 সফলভাবে মেসেজ গেলে ডাটাবেজে লগ সেভ
                    SMSLog.objects.create(
                        student_name=student.name,
                        phone=student.phone,
                        message=custom_message,
                        sms_type='approval',
                        status='success'
                    )
                else:
                    sms_error_reason = api_message

                    # 🎯 এপিআই ফেইল্ড হলে ফেইল্ড স্ট্যাটাস ও কারণসহ লগ সেভ
                    SMSLog.objects.create(
                        student_name=student.name,
                        phone=student.phone,
                        message=custom_message,
                        sms_type='approval',
                        status='failed',
                        error_message=api_message
                    )
            else:
                sms_error_reason = "স্টুডেন্টের মোবাইল নাম্বার পাওয়া যায়নি।"

                # 🎯 মোবাইল নাম্বার না থাকলেও ট্র্যাকিংয়ের জন্য ফেইল্ড লগ সেভ
                SMSLog.objects.create(
                    student_name=student.name,
                    phone="N/A",
                    message=custom_message,
                    sms_type='approval',
                    status='failed',
                    error_message=sms_error_reason
                )

        except Exception as e:
            sms_error_reason = str(e)

            # 🎯 কোডে কোনো সিস্টেম এক্সেপশন বা এরর আসলেও তা সেভ হবে
            SMSLog.objects.create(
                student_name=student.name,
                phone=student.phone if student.phone else "N/A",
                message=custom_message if custom_message else "Error system failed to generate message.",
                sms_type='approval',
                status='failed',
                error_message=sms_error_reason
            )

        # মেসেজ নোটিফিকেশন হ্যান্ডেলিং
        if sms_sent:
            messages.success(request, f"{student.name}-এর ভর্তি অ্যাপ্রুভ করা হয়েছে এবং সেটিংসের টেমপ্লেট অনুযায়ী কনফার্মেশন এসএমএস পাঠানো হয়েছে।")
        else:
            messages.success(request, f"{student.name}-এর ভর্তি অ্যাপ্রুভ করা হয়েছে।")
            messages.error(request, f"⚠️ এসএমএস পাঠানো যায়নি! কারণ: {sms_error_reason}")

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
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class StudentCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        student_phone = form.cleaned_data.get('phone')
        student_email = form.cleaned_data.get('email')
        student_name = form.cleaned_data.get('name')

        # 🛑 ১. OneToOne constraint চেক (ইউজার অলরেডি অন্য কোনো স্টুডেন্টের সাথে যুক্ত কিনা)
        if student_phone:
            user_instance = User.objects.filter(username=student_phone).first()
            if user_instance and hasattr(user_instance, 'student_profile'):
                # ফর্মের মোবাইল নাম্বার ফিল্ডে সরাসরি এরর পাস করা হলো
                form.add_error('phone', "এই মোবাইল নাম্বারের ইউজার অ্যাকাউন্টটি ইতিমধ্যে অন্য একজন স্টুডেন্টের সাথে যুক্ত!")
                return self.form_invalid(form)
        else:
            messages.error(self.request, "স্টুডেন্টের মোবাইল নাম্বার পাওয়া যায়নি!")
            return self.form_invalid(form)

        # ২. ফর্মের ডেটা মেমরিতে হোল্ড করা
        student = form.save(commit=False)

        # 💡 স্বয়ংক্রিয়ভাবে স্টুডেন্ট আইডি (Student ID) তৈরি করার লজিক
        last_student = Student.objects.all().order_by('id').last()
        if last_student and last_student.student_id:
            try:
                student.student_id = str(int(last_student.student_id) + 1)
            except ValueError:
                student.student_id = "780"
        else:
            student.student_id = "780"

        # ৩. অটোমেটিক সেশন ও স্ট্যাটাস সেট করা
        current_year = datetime.now().year
        next_year = current_year + 1
        student.session = f"{current_year}-{next_year}"
        student.status = 'pending'

        # ৪. ইউজার অ্যাকাউন্ট তৈরি বা লিঙ্ক করার লজিক
        if not user_instance:
            # নতুন ইউজার তৈরি (ইউজারনেম এবং পাসওয়ার্ড দুটোই ফোন নাম্বার)
            user_instance = User.objects.create_user(
                username=student_phone,
                password=student_phone,
                email=student_email if student_email else '',
                first_name=student_name
            )

        # ইউজার অ্যাকাউন্টটি স্টুডেন্টের ওয়ান-টু-ওয়ান ফিল্ডে লিঙ্ক করা হলো
        student.account = user_instance

        # ৫. ডেটাবেজে ফাইনাল স্টুডেন্ট সেভ
        student.save()

        # ৬. এসএমএস পাঠানোর লজিক
        sms_sent = False
        sms_error_reason = "Unknown Error"

        try:
            settings_instance = AttendenceSetting.objects.first()
            if settings_instance and settings_instance.reg_sms:
                custom_message = settings_instance.reg_sms
                custom_message = custom_message.replace("[name]", student.name)
                custom_message = custom_message.replace("[phone]", student_phone)

                is_success, api_message = send_sms(student_phone, custom_message)
                if is_success:
                    sms_sent = True
                else:
                    sms_error_reason = api_message
            else:
                sms_error_reason = "SMS Settings অথবা টেমপ্লেট ডাটাবেজে কনফিগার করা নেই।"
        except Exception as e:
            sms_error_reason = str(e)

        # ৭. ডাইনামিক স্ক্রিন মেসেজ
        if sms_sent:
            messages.success(self.request, f"স্টুডেন্ট {student.name} সফলভাবে তৈরি হয়েছে! আইডি: {student.student_id} এবং স্বাগতম এসএমএস পাঠানো হয়েছে")
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
