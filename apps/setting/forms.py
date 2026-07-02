from django import forms

from .models import AttendenceSetting


class AttendanceSettingForm(forms.ModelForm):
    class Meta:
        model = AttendenceSetting
        # 🟢 fields লিস্টে 'reg_sms' ইনক্লুড করা হলো
        fields = ['website_name', 'send_id_token', 'reg_sms']
        widgets = {
            'website_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your institute name here...'
            }),
            'send_id_token': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your unique ID token here...'
            }),
            # 🟢 'reg_sms' এর জন্য টেক্সট এরিয়া উইজেট বুটস্ট্র্যাপ ক্লাস ও বাংলা প্লেসহোল্ডার সহ
            'reg_sms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'মেসেজ লিখতে [name] এবং [phone] শর্টকোডগুলো ব্যবহার করুন...'
            }),
        }
        labels = {
            'website_name': 'Sender ID',
            'send_id_token': 'Token',
            'reg_sms': 'Student Registration SMS Template (বাংলা)'
        }
