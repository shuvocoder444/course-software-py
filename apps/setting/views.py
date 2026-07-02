# views.py (আপনার অ্যাপ ফোল্ডারের ভেতর)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from apps.account.views import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin

from .forms import InstituteSettingForm

# আপনার প্রজেক্টের মিক্সিন, মডেল এবং ফর্ম ইমপোর্ট করুন
from .models import InstituteSetting


# --- ১. INSTITUTE SETTING VIEW & UPDATE ---
class InstituteSettingView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = InstituteSetting
    form_class = InstituteSettingForm
    template_name = 'institute_settings.html'
    success_url = reverse_lazy('institute')  # রিডাইরেক্ট হবে 'institute' ইউআরএল-এ

    def get_object(self, queryset=None):
        """
        ডাটাবেজে যদি আগে থেকে কোনো রেকর্ড না থাকে,
        তবে এটি ক্র্যাশ না করে স্বয়ংক্রিয়ভাবে ID=1 দিয়ে একটি নতুন রো তৈরি করে নিবে।
        """
        obj, created = InstituteSetting.objects.get_or_create(id=1)
        return obj

    def get_context_data(self, **kwargs):
        """টেমপ্লেটে অতিরিক্ত ডেটা পাঠানোর জন্য"""
        context = super().get_context_data(**kwargs)
        context['setting_data'] = self.object
        context['title'] = 'Institute Settings Dashboard Panel'
        context['layout_path'] = 'layouts/master.html'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Institute configuration profile updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update configuration. Please check the form errors.")
        return super().form_invalid(form)


# --- ২. INSTITUTE SETTING DELETE VIEW ---
class InstituteSettingDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    """
    ইনস্টিটিউট কনফিগারেশন প্রোফাইল ডিলিট করার ভিউ।
    নিরাপত্তার স্বার্থে এটি শুধুমাত্র POST রিকোয়েস্ট গ্রহণ করবে।
    """
    def post(self, request, pk, *args, **kwargs):
        setting_record = get_object_or_404(InstituteSetting, pk=pk)
        setting_record.delete()

        messages.warning(request, "Institute configuration profile deleted successfully!")
        return redirect('institute')
