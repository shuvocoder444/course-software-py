from django import forms
from .models import AttendenceSetting

class AttendanceSettingForm(forms.ModelForm):
    class Meta:
        model = AttendenceSetting
        # 🟢 fields লিস্টে নতুন ফিল্ড 'payment_sms' ইনক্লুড করা হলো
        fields = ['website_name', 'send_id_token', 'reg_sms', 'approve_sms', 'payment_sms']

        widgets = {
            'website_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your institute name here...'
            }),
            'send_id_token': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your unique ID token here...'
            }),
            'reg_sms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'cols': '80',
                'placeholder': 'মেসেজ লিখতে [name] এবং [phone] শর্টকোডগুলো ব্যবহার করুন...'
            }),
            'approve_sms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'cols': '80',
                'placeholder': 'মেসেজ লিখতে [name] শর্টকোড ব্যবহার করুন...'
            }),
            # 🎯 নতুন যুক্ত করা পেমেন্ট এসএমএস উইজেট (বুটস্ট্র্যাপ ক্লাস ও বাংলা প্লেসহোল্ডার সহ)
            'payment_sms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'cols': '80',
                'placeholder': 'মেসেজ লিখতে [name], [amount] এবং [invoice] শর্টকোডগুলো ব্যবহার করুন...'
            }),
        }

        labels = {
            'website_name': 'Sender ID',
            'send_id_token': 'Token',
            'reg_sms': 'Student Registration SMS Template (বাংলা)',
            'approve_sms': 'Student Approval Confirmation SMS Template (বাংলা)',
            # 🎯 নতুন যুক্ত করা পেমেন্ট এসএমএস লেবেল
            'payment_sms': 'Student Payment Confirmation SMS Template (বাংলা)'
        }



from django import forms
from .models import SiteSetting

class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        # সব ফিল্ড ফর্মে রাখার জন্য '__all__' ব্যবহার করা হয়েছে
        fields = '__all__'

        # প্রতিটি ফিল্ডের জন্য বুটস্ট্র্যাপ ক্লাস ও প্লেসহোল্ডার সেট করা হয়েছে
        widgets = {
            'institution_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'প্রতিষ্ঠানের নাম লিখুন'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ইমেইল ঠিকানা'}),
            'post_office': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'পোস্ট অফিস'}),
            'upozila': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'উপজেলা'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'জেলা'}),
            'eiin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EIIN নম্বর'}),
            'school_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'স্কুল কোড (ঐচ্ছিক)'}),
            'established_at': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'স্থাপিত সাল (যেমন: ১৯২৯)'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ফোন নম্বর'}),
            'map_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'গুগল ম্যাপ লিংক (ঐচ্ছিক)'}),

            # উইকেন্ডের চেকবক্সগুলোর ডিজাইন
            'friday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'saturday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sunday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'monday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tuesday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wednesday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'thursday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # মিডিয়া/ফাইল আপলোডের ফিল্ডসমূহ
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'favicon': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'student_admission_pdf_banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'invoice_pdf_banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        } # 👈 এই ক্লোজিং ব্র্যাকেটটি আপনার কোডে মিসিং ছিল!
