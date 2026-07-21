from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

# আপনার প্রোজেক্টের থিম হেল্পার ইম্পোর্ট
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from .decorators import role_required
from .forms import AccountCreationForm
from .models import Account

# ==============================================================================
#  ১. কাস্টম মিক্সিন এবং হেল্পার ফাংশন (Vuxy Template Layout & Security) - FIXED
# ==============================================================================

def get_menu_file_by_role(role):
    """ইউজারের রোল অনুযায়ী নির্দিষ্ট JSON মেনু ফাইলের নাম রিটার্ন করে"""
    role_menu_map = {
        'ADMIN': 'vertical_admin_menu.json',
        'TEACHER': 'vertical_teacher_menu.json',
        'STUDENT': 'vertical_student_menu.json',
        'RECEPTION': 'vertical_reception_menu.json',
        'ACCOUNTS': 'vertical_accounting_menu.json',
    }
    return role_menu_map.get(role, 'vertical_menu.json')


class VuxyVerticalLayoutMixin:
    """Vuxy টেমপ্লেটের ভার্টিক্যাল লেআউট এবং ডাইনামিক মেনু লোড করার জন্য কাস্টম মিক্সিন (CBV এর জন্য)"""
    def get_context_data(self, **kwargs):
        # প্রথমে বেস কনটেক্সট তৈরি করা
        base_context = super().get_context_data(**kwargs)

        # 👑 ফিক্স: লেআউট ইনিশিয়াল করার আগেই কনটেক্সটে user অবজেক্ট পাস করা হলো
        base_context.update({
            "user": self.request.user
        })

        context = TemplateLayout.init(self, base_context)

        # লগইন করা ইউজারের রোল অনুযায়ী মেনু সিলেক্ট করা হচ্ছে
        user_role = getattr(self.request.user, 'role', None)
        menu_file = get_menu_file_by_role(user_role)

        context.update({
            "layout": "vertical",
            "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            "menu_file": menu_file,
        })
        return context


def get_vuxy_context(view_instance_or_request, extra_context=None):
    """ফাংশন-বেসড ভিউতে (FBV) Vuxy লেআউট ও ডাইনামিক মেনু সহজে লোড করার জন্য হেল্পার ফাংশน"""
    if extra_context is None:
        extra_context = {}

    # 👑 ফিক্স: এক্সট্রা কনটেক্সটে কারেন্ট রিকোয়েস্টের user অবজেক্ট পুশ করা হলো
    extra_context.update({
        "user": view_instance_or_request.user
    })

    # প্রথম প্যারামিটারে অবজেক্ট পাস করার জন্য ডামি ক্লাস
    class DummyView:
        request = view_instance_or_request

    context = TemplateLayout.init(DummyView(), extra_context)

    # রিকোয়েস্ট থেকে ইউজারের রোল বের করে মেনু ফাইল নির্ধারণ
    user_role = getattr(view_instance_or_request.user, 'role', None)
    menu_file = get_menu_file_by_role(user_role)

    context.update({
        "layout": "vertical",
        "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        "menu_file": menu_file,
    })
    return context


class AdminRoleRequiredMixin:
    """শুধুমাত্র ADMIN রোল ভেরিফাই করার জন্য সিকিউরিটি মিক্সিন"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'ADMIN':
            messages.error(request, "You are not authorized to view this page.")
            if not request.user.is_authenticated:
                return redirect('login')
            return redirect('dashboard_redirect')
        return super().dispatch(request, *args, **kwargs)

from django.contrib.auth.views import LoginView, LogoutView

# ==============================================================================
# ২. ফ্রন্টএন্ড/গেস্ট লগইন এবং লগআউট কন্ট্রোলার (CBV)
# ==============================================================================

class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'auth/login.html'  # আপনার বর্তমান টেমপ্লেট পাথ অনুযায়ী ঠিক আছে

    def get_success_url(self):
        # লগইন সফল হলে ড্যাশবোর্ডে রিডাইরেক্ট করবে
        return reverse_lazy('dashboard_redirect')

    def dispatch(self, request, *args, **kwargs):
        # ইউজার যদি অলরেডি লগইন করা থাকে, তবে তাকে ড্যাশবোর্ডে পাঠিয়ে দেবে
        if request.user.is_authenticated:
            return redirect('dashboard_redirect')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # ১. গ্লোবাল লেআউট ইনিশিয়ালাইজ করা
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # ২. কনটেক্সট আপডেট করে ফ্রন্টএন্ড লেআউট ('layout_front.html') সেট করা
        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,
            }
        )

        # ৩. ম্যাপ কনটেক্সট রান করা
        TemplateHelper.map_context(context)

        return context

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f"Welcome back, {user.username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    # Django 5.0+ এ LogoutView-এর রিডাইরেক্ট করার জন্য 'next_page' ব্যবহার করা সবচেয়ে ভালো ও নিরাপদ পদ্ধতি
    next_page = reverse_lazy('login')  # ❌ এখানে থাকা অতিরিক্ত স্পেসটি ('login ') দূর করা হয়েছে

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)
# ==============================================================================
#  ৩. ডাইনামিক রাউটার ভিউ (রোল অনুযায়ী রিডাইরেক্ট)
# ==============================================================================

@login_required
def dashboard_redirect_view(request):
    role = request.user.role
    if role == 'ADMIN':
        return redirect('admin_dashboard')
    elif role == 'TEACHER':
        return redirect('teacher_dashboard')
    elif role == 'STUDENT':
        return redirect('student_dashboard')
    elif role == 'RECEPTION':
        return redirect('reception_dashboard')
    elif role == 'ACCOUNTS':
        return redirect('accounting_dashboard')
    else:
        return redirect('login')


# ==============================================================================
#  ৪. ৫টি আলাদা সিকিউরড ড্যাশবোর্ড ভিউ (মেনু অটোমেটিক ডাইনামিক হবে)
# ==============================================================================

# Admin Dashboard
@login_required
@role_required(allowed_roles=['ADMIN'])
def admin_dashboard(request):
    context = get_vuxy_context(request)
    return render(request, 'dashboards/admin.html', context)


# Teacher Dashboard
@login_required
@role_required(allowed_roles=['TEACHER'])
def teacher_dashboard(request):
    context = get_vuxy_context(request)
    return render(request, 'dashboards/teacher.html', context)


# Student Dashboard
@login_required
@role_required(allowed_roles=['STUDENT'])
def student_dashboard(request):
    context = get_vuxy_context(request)
    return render(request, 'dashboards/student.html', context)


# Reception Dashboard
@login_required
@role_required(allowed_roles=['RECEPTION'])
def reception_dashboard(request):
    context = get_vuxy_context(request)
    return render(request, 'dashboards/reception.html', context)


# Accounts (Accounting) Dashboard
@login_required
@role_required(allowed_roles=['ACCOUNTS'])
def accounting_dashboard(request):
    context = get_vuxy_context(request)
    return render(request, 'dashboards/accounting.html', context)


# ==============================================================================
#  ৫. ইউজার ম্যানেজমেন্ট CRUD ভিউ (CBV - Admin Only)
# ==============================================================================

# ১. USER LIST VIEW
class UserListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Account
    template_name = 'dashboards/user_list.html'
    context_object_name = 'users'
    ordering = ['-id']


# ২. CREATE USER VIEW
class UserCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Account
    form_class = AccountCreationForm
    template_name = 'dashboards/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New User'
        return context

    def form_valid(self, form):
        messages.success(self.request, "User created successfully!")
        return super().form_valid(form)


# ৩. EDIT USER VIEW
class UserEditView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = Account
    form_class = AccountCreationForm
    template_name = 'dashboards/user_form.html'
    success_url = reverse_lazy('user_list')
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit User'
        return context

    def form_valid(self, form):
        messages.success(self.request, "User updated successfully!")
        return super().form_valid(form)


# ৪. DELETE USER VIEW
class UserDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk):
        user_instance = get_object_or_404(Account, pk=pk)

        if request.user.id == user_instance.id:
            messages.error(request, "You cannot delete your own admin account!")
        else:
            user_instance.delete()
            messages.success(request, "User deleted successfully!")

        return redirect('user_list')

    def get(self, request, pk):
        return self.post(request, pk)






# ==========================================  admin_dashboard  ================================


from django.contrib.auth import get_user_model

from apps.students.models import Student
from apps.courses.models import Course

Account = get_user_model() # আপনার ইউজার অ্যাকাউন্ট মডেল পেতে

@login_required
@role_required(allowed_roles=['ADMIN'])
def admin_dashboard(request):
    # ডাইনামিকালি ডাটাবেজ থেকে রিয়েল কাউন্ট নিয়ে আসা হচ্ছে
    total_students = Student.objects.count()
    total_teachers = Account.objects.filter(role='TEACHER').count()
    total_users = Account.objects.count()

    # সাম্প্রতিক রেজিস্টার্ড ৩ জন স্টুডেন্টকে লিস্টে দেখানোর জন্য
    recent_students = Student.objects.order_by('-id')[:3]

    # Vuxy কন্টেক্সট লোড করা হচ্ছে এবং আমাদের ডাইনামিক ডাটাগুলো পাস করা হচ্ছে
    extra_context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_users': total_users,
        'recent_students': recent_students,
    }

    context = get_vuxy_context(request, extra_context=extra_context)
    return render(request, 'dashboards/admin.html', context)


# ==========================================   student_dashboard   ================================



@login_required
@role_required(allowed_roles=['STUDENT'])
def student_dashboard(request):
    """
    লগইন করা স্টুডেন্টের প্রোফাইল, রানিং ব্যাচ, এনরোল করা সমস্ত কোর্স,
    স্টুডেন্টের দেওয়া রিভিউ এবং অন্যান্য উপলব্ধ কোর্সগুলো ডাইনামিকালি লোড করার ভিউ।
    """
    student = None
    batch = None
    enrolled_courses = []
    enrolled_course_ids = []
    my_reviews = []
    other_courses = Course.objects.all()

    try:
        # ১. লগইন করা ইউজারের সাথে যুক্ত স্টুডেন্ট প্রোফাইল খোঁজা
        student = request.user.student_profile

        if student:
            # ২. স্টুডেন্টের ব্যাচ খোঁজা
            batch = getattr(student, 'batch', None)

            # ৩. Enrollment মডেল থেকে স্টুডেন্টের সচল (active) কোর্সগুলো বের করা
            active_enrollments = student.enrollments.filter(is_active=True).select_related('course')
            enrolled_courses = [enrollment.course for enrollment in active_enrollments]

            # ৪. এনরোল করা কোর্সের আইডিগুলো আলাদা করা (Other Courses ফিল্টার করার জন্য)
            enrolled_course_ids = [course.id for course in enrolled_courses]

            # ৫. স্টুডেন্ট যে কোর্সগুলোতে অলরেডি আছে, সেগুলো বাদে বাকি কোর্সগুলো আনা হচ্ছে
            other_courses = Course.objects.exclude(id__in=enrolled_course_ids)

            # ৬. এই স্টুডেন্টের দেওয়া সমস্ত কোর্স রিভিউ নিয়ে আসা
            my_reviews = CourseReview.objects.filter(user=request.user).select_related('course')

    except (Student.DoesNotExist, AttributeError):
        student = None

    # কনটেক্সটে নতুন ডেটাগুলো পাস করা হলো
    extra_context = {
        "student": student,
        "batch": batch,
        "enrolled_courses": enrolled_courses, # এখন একাধিক কোর্স সাপোর্ট করবে
        "my_reviews": my_reviews,             # স্টুডেন্টের নিজস্ব রিভিউসমূহ
        "other_courses": other_courses[:4],   # ড্যাশবোর্ডে দেখানোর জন্য ৪টি লিমিট
        "title": "Student Dashboard"
    }

    # Vuxy লেআউট ও মেনুসহ কনটেক্সট জেনারেট করা
    context = get_vuxy_context(request, extra_context=extra_context)

    return render(request, "dashboards/student.html", context)



from django.contrib.auth.decorators import login_required
from apps.courses.models import Enrollment, CourseReview  # আপনার প্রজেক্টের সঠিক পাথ অনুযায়ী মডেল ইমপোর্ট করুন
# প্রজেক্টের ভেক্সাটাইল লেআউট কনটেক্সট ফাংশন ইমপোর্ট
# from আপনার_অ্যপ.utils import get_vuxy_context (আপনার সঠিক পাথ অনুযায়ী রাখুন)

@login_required
def student_course_single(request, slug):
    course = get_object_or_404(Course, slug=slug)

    has_enrolled = False
    is_enrollment_active = False

    try:
        student = request.user.student_profile
        # ডেটাবেস থেকে স্পেসিফিক এনরোলমেন্ট রেকর্ড চেক করা
        enrollment = Enrollment.objects.filter(student=student, course=course).first()

        if enrollment:
            has_enrolled = True
            is_enrollment_active = enrollment.is_active

        # যদি ব্যাচের মাধ্যমে সরাসরি এনরোলড থাকে
        if not has_enrolled and getattr(student, 'batch', None):
            if student.batch.course == course:
                has_enrolled = True
                is_enrollment_active = True  # ব্যাচ এসাইন থাকলে সেটি সরাসরি একটিভ

    except AttributeError:
        pass

    # কোর্সের সব রিভিউ নিয়ে আসা
    reviews = course.reviews.all().order_by('-created_at')

    # এক্সট্রা কনটেক্সট তৈরি
    extra_context = {
        'course': course,
        'has_enrolled': has_enrolled,
        'course_enrollment_status_is_active': is_enrollment_active,  # এই ভ্যারিয়েবলটি HTML কন্ডিশনে কাজ করবে
        'reviews': reviews,
        'title': course.name
    }

    # Vuxy লেআউট ও মেনুসহ মেইন কনটেক্সট জেনারেট করা
    context = get_vuxy_context(request, extra_context=extra_context)
    return render(request, "dashboards/studentcourse-single.html", context)


@login_required
def buy_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    try:
        student = request.user.student_profile

        # ইতিমধ্যে রিকোয়েস্ট করা আছে কিনা চেক
        existing_enrollment = Enrollment.objects.filter(student=student, course=course).first()

        if existing_enrollment:
            if existing_enrollment.is_active:
                messages.warning(request, "আপনি ইতিমধ্যে এই কোর্সটি কিনেছেন এবং এটি একটিভ আছে।")
            else:
                messages.info(request, "এই কোর্সের জন্য আপনার অনুরোধটি ইতিমধ্যে অ্যাডমিন এপ্রুভালের জন্য পেন্ডিং আছে।")
        else:
            # ডিফল্টভাবে is_active=False দেওয়া হলো (অর্থাৎ অ্যাডমিন এপ্রুভ করার আগে পেন্ডিং থাকবে)
            Enrollment.objects.create(student=student, course=course, is_active=False)
            messages.success(request, f"সফলভাবে {course.name} কোর্সের জন্য অনুরোধ পাঠানো হয়েছে। অ্যাডমিন এপ্রুভ করলে ড্যাশবোর্ডে দেখতে পাবেন।")

    except AttributeError:
        messages.error(request, "আপনার কোনো স্টুডেন্ট প্রোফাইল পাওয়া যায়নি।")

    return redirect('student_course_single', slug=course.slug)


@login_required
def add_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # ডাটাবেসে রিভিউ সেভ করা
        CourseReview.objects.create(
            user=request.user,
            course=course,
            rating=rating,
            comment=comment
        )

        messages.success(request, "আপনার রিভিউটি সফলভাবে যুক্ত করা হয়েছে।")
        return redirect('student_course_single', slug=course.slug)

    return redirect('student_course_single', slug=course.slug)




from django.contrib.auth.decorators import login_required

@login_required
def edit_review(request, review_id):
    """
    স্টুডেন্ট নিজের দেওয়া রিভিউ এডিট করার ভিউ
    """
    review = get_object_or_404(CourseReview, id=review_id, user=request.user)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            review.rating = rating
            review.comment = comment
            review.save()
            messages.success(request, "আপনার রিভিউটি সফলভাবে আপডেট করা হয়েছে।")
        else:
            messages.error(request, "সবগুলো ফিল্ড সঠিকভাবে পূরণ করুন।")

        return redirect('student_course_single', slug=review.course.slug)

    return redirect('student_course_single', slug=review.course.slug)


@login_required
def delete_review(request, review_id):
    """
    স্টুডেন্ট নিজের দেওয়া রিভিউ ডিলিট করার ভিউ
    """
    review = get_object_or_404(CourseReview, id=review_id, user=request.user)
    course_slug = review.course.slug

    review.delete()
    messages.success(request, "আপনার রিভিউটি সফলভাবে ডিলিট করা হয়েছে।")

    return redirect('student_course_single', slug=course_slug)



# ==========================================   student_dashboard  End  ================================




from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db import transaction
from .models import Account, SMSVerification
from .forms import OTPRegistrationForm
from .models import Account
from apps.setting.utils import send_sms
from datetime import datetime  # 🎯
from .models import Account




class StudentAjaxRegisterView(TemplateView):
    template_name = 'auth/register.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,
                "form": OTPRegistrationForm(),
            }
        )
        TemplateHelper.map_context(context)
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        # ---------------- STEP 1: SEND OTP ----------------
        if action == 'send_otp':
            form = OTPRegistrationForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data['phone_number']

                if Account.objects.filter(username=phone_number).exists():
                    return JsonResponse({
                        'status': 'error',
                        'message': 'এই ফোন নম্বরটি দিয়ে ইতিমধ্যে নিবন্ধন করা হয়েছে।'
                    })

                # Session dynamic storage
                request.session['reg_full_name'] = form.cleaned_data['full_name']
                request.session['reg_phone_number'] = phone_number
                request.session['reg_password'] = form.cleaned_data['password']

                # OTP creation (Testing-এর জন্য "1234")
                otp_code = "1234"
                otp_message = f"Your JBD IT Registration OTP is: {otp_code}. Do not share this with anyone."

                SMSVerification.objects.create(
                    phone_number=phone_number,
                    otp_code=otp_code,
                    is_used=False
                )

                is_sent, sms_response_msg = send_sms(phone_number, otp_message)

                if is_sent:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'আপনার ফোনে একটি ওটিপি (OTP) পাঠানো হয়েছে।'
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'ওটিপি পাঠানো যায়নি। API Error: {sms_response_msg}'
                    })
            else:
                errors_dict = {}
                for field, error_list in form.errors.items():
                    errors_dict[field] = [{'message': error_list[0]}]

                return JsonResponse({
                    'status': 'error',
                    'errors': errors_dict
                })

        # ---------------- STEP 2: VERIFY OTP & CREATE USER ----------------
        elif action == 'verify_otp':
            otp_code = request.POST.get('otp_code')
            phone_number = request.session.get('reg_phone_number')
            full_name = request.session.get('reg_full_name', '')
            password = request.session.get('reg_password')

            if not phone_number or not password:
                return JsonResponse({
                    'status': 'error',
                    'message': 'নিবন্ধন সেশন শেষ হয়ে গেছে। অনুগ্রহ করে আবার চেষ্টা করুন।'
                })

            verification = SMSVerification.objects.filter(
                phone_number=phone_number,
                otp_code=otp_code,
                is_used=False
            ).first()

            if verification:
                try:
                    # সার্কুলার ডিপেন্ডেন্সি এড়াতে এখানে লোকাল ইমপোর্ট করা হলো
                    from apps.students.models import Student

                    with transaction.atomic():
                        verification.is_used = True
                        verification.save()

                        # নাম split করা
                        name_parts = full_name.split(' ', 1)
                        first_name = name_parts[0]
                        last_name = name_parts[1] if len(name_parts) > 1 else ''

                        # অ্যাকাউন্ট তৈরি
                        user, created = Account.objects.get_or_create(
                            username=phone_number,
                            defaults={
                                'first_name': first_name,
                                'last_name': last_name,
                                'role': 'STUDENT',
                                'is_active': True
                            }
                        )

                        if created:
                            user.set_password(password)
                            user.save()

                            # 🎯 স্বয়ংক্রিয়ভাবে স্টুডেন্ট আইডি (Student ID) তৈরি করার লজিক (780 থেকে শুরু)
                            last_student = Student.objects.all().order_by('id').last()
                            if last_student and last_student.student_id:
                                try:
                                    next_id = str(int(last_student.student_id) + 1)
                                except ValueError:
                                    next_id = "780"
                            else:
                                next_id = "780"

                            # 🎯 বর্তমান বছরের উপর ভিত্তি করে সেশন তৈরি (যেমন: 2026-2027)
                            current_year = datetime.now().year
                            next_year = current_year + 1
                            generated_session = f"{current_year}-{next_year}"

                            # স্টুডেন্ট প্রোফাইল তৈরি
                            Student.objects.get_or_create(
                                account=user,
                                defaults={
                                    'student_id': next_id,       # 🎯 ডাইনামিক সিরিয়াল আইডি
                                    'name': full_name,
                                    'phone': phone_number,
                                    'session': generated_session,# 🎯 ডাইনামিক সেশন বছর
                                    'status': 'pending'
                                }
                            )

                    # অটো লগইন
                    authenticated_user = authenticate(username=phone_number, password=password)
                    if authenticated_user is not None:
                        login(request, authenticated_user)

                    # সেশন ডাটা রিমুভ
                    request.session.pop('reg_full_name', None)
                    request.session.pop('reg_phone_number', None)
                    request.session.pop('reg_password', None)

                    messages.success(request, "নিবন্ধন সফল হয়েছে!")
                    return JsonResponse({
                        'status': 'verified',
                        'redirect_url': '/dashboard/account/student/'
                    })
                except Exception as e:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'রেজিস্ট্রেশন প্রсеসিং ব্যর্থ হয়েছে: {str(e)}'
                    })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'ভুল অথবা মেয়াদোত্তীর্ণ ওটিপি কোড।'
                })

        return JsonResponse({'status': 'error', 'message': 'Invalid Action Submissions'})
