
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.account.decorators import role_required
from apps.account.views import get_vuxy_context

from .forms import AttendanceSettingForm
from .models import AttendenceSetting
# role_required এবং get_vuxy_context আপনার প্রজেক্টের সঠিক পাথ থেকে ইমপোর্ট করবেন
# from apps.core.decorators import role_required
# from apps.core.utils import get_vuxy_context


@login_required
@role_required(allowed_roles=['ADMIN'])
def institute_settings_view(request):
    # ডাটাবেজ থেকে প্রথম অবজেক্টটি তুলে আনা হচ্ছে
    setting_instance = AttendenceSetting.objects.first()

    if request.method == 'POST':
        # instance=setting_instance দেওয়ার কারণে ডাটা থাকলে আপডেট হবে, না থাকলে নতুন ক্রিয়েট হবে।
        # আমাদের আপডেট করা AttendanceSettingForm এখানে সরাসরি নতুন ফিল্ড সহ ডেটা রিসিভ করবে।
        form = AttendanceSettingForm(request.POST, instance=setting_instance)
        if form.is_valid():
            form.save()
            if setting_instance:
                messages.success(request, "Settings updated successfully!")
            else:
                messages.success(request, "Settings saved successfully!")
            return redirect('institute_settings')
        else:
            messages.error(request, "Something went wrong. Please check your input.")
    else:
        # GET রিকোয়েস্টে যদি আগে থেকে ডাটা থাকে তবে ফর্মে নতুন ফিল্ডসহ ডাটা লোড হবে
        form = AttendanceSettingForm(instance=setting_instance)

    extra_context = {
        'form': form,
        'setting': setting_instance,
    }

    # Vuxy টেমপ্লেট লেআউট কনটেক্সট লোড করা
    context = get_vuxy_context(request, extra_context=extra_context)
    return render(request, 'attendance.html', context)



from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import SMSLog

# ১. এসএমএস হিস্টোরি ভিউ (পেজে ১০০টি করে দেখাবে)
class SMSHistoryListView(LoginRequiredMixin, ListView):
    model = SMSLog
    template_name = 'sms_history.html'
    context_object_name = 'sms_logs'
    paginate_by = 100  # 🎯 প্রতি পেজে ১০০টি ডাটা থাকবে

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vuxy_context = get_vuxy_context(self.request, extra_context=context)
        return vuxy_context

# 🎯 ২. বাল্ক ও সিঙ্গেল ডিলিট হ্যান্ডেল করার জন্য নতুন ভিউ
class SMSLogDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # টেমপ্লেট থেকে সিলেক্ট করা আইডিগুলোর লিস্ট নেওয়া
        log_ids = request.POST.getlist('log_ids')

        if log_ids:
            # একসাথে সবগুলো সিলেক্টেড লগ ডিলিট করা
            deleted_count, _ = SMSLog.objects.filter(id__in=log_ids).delete()
            messages.success(request, f"সফলভাবে {deleted_count}টি এসএমএস লগ ডিলিট করা হয়েছে।")
        else:
            messages.warning(request, "ডিলিট করার জন্য কোনো লগ সিলেক্ট করা হয়নি!")

        return redirect('sms_history')



from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from apps.account.views import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin
from .models import SiteSetting
from .forms import SiteSettingForm

class UpdateSiteSettingsView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = SiteSetting
    form_class = SiteSettingForm
    template_name = 'settings_form.html'
    success_url = reverse_lazy('update_site_settings')

    def get_object(self, queryset=None):
        instance = SiteSetting.objects.first()
        if not instance:
            instance = SiteSetting.objects.create()
        return instance

    def form_valid(self, form):
        try:
            with transaction.atomic():
                site_setting = form.save(commit=False)
                site_setting.save()
                form.save_m2m()

            messages.success(self.request, "Site settings updated successfully!")
            return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f"⚠️ সেটিংস আপডেট করা যায়নি! কারণ: {str(e)}")
            # রিকার্সন এরর এড়াতে super ফর্মে পাঠানো হলো
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ফর্মে ভুল রয়েছে! দয়া করে সঠিক তথ্য প্রদান করুন।")
        return super().form_invalid(form)
