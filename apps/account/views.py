from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, View

# আপনার প্রোজেক্টের থিম হেল্পার ইম্পোর্ট
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from .models import Account
from .forms import AccountCreationForm
from .decorators import role_required

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




# আপনার প্রজেক্টের নির্দিষ্ট হেল্পার ক্লাসগুলো ইমপোর্ট করুন (প্রয়োজন অনুযায়ী পাথ ঠিক করে নিবেন)
# from .helpers import TemplateLayout, TemplateHelper


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





from django.contrib.auth import get_user_model
from apps.students.models import Student  # স্টুডেন্ট মডেল ইম্পোর্ট করুন

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
