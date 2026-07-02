
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.account.decorators import role_required
from apps.account.views import get_vuxy_context

from .forms import AttendanceSettingForm
from .models import AttendenceSetting


@login_required
@role_required(allowed_roles=['ADMIN'])
def institute_settings_view(request):
    setting_instance = AttendenceSetting.objects.first()

    if request.method == 'POST':
        # instance=setting_instance দেওয়ার কারণে ডাটা থাকলে আপডেট হবে, না থাকলে নতুন ক্রিয়েট হবে
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
        # GET রিকোয়েস্টে যদি আগে থেকে ডাটা থাকে তবে ফর্মে ডাটা লোড হবে, না হয় খালি ফর্ম দেখাবে
        form = AttendanceSettingForm(instance=setting_instance)

    extra_context = {
        'form': form,
        'setting': setting_instance,
    }

    # Vuxy টেমপ্লেট লেআউট কনটেক্সট লোড করা
    context = get_vuxy_context(request, extra_context=extra_context)
    return render(request, 'attendance.html', context)
