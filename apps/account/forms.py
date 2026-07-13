# apps/account/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account  # একই অ্যাপের অ্যাকাউন্ট মডেল ইম্পোর্ট করা হলো

class AccountCreationForm(UserCreationForm):
    """Vuxy থিম ও কাস্টম রোল সাপোর্টেড কাস্টম অ্যাকাউন্ট ক্রিয়েশন ফর্ম"""

    class Meta:
        model = Account
        # জ্যাঙ্গো ইউজার তৈরিতে সাধারণত যে ফিল্ডগুলো লাগে + আপনার কাস্টম 'role' ফিল্ড
        fields = ['username', 'first_name', 'last_name', 'email', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Vuxy / Bootstrap ৫ ক্লাসের সাথে ম্যাচ করানোর জন্য অটো-স্টাইলিং লজিক
        for field_name, field in self.fields.items():
            # ডাইনামিক প্লেসহোল্ডার সেট করা
            field.widget.attrs.update({
                'placeholder': f'Enter {field.label.lower() if field.label else field_name}'
            })

            # চয়েস ফিল্ডের (role) জন্য form-select এবং বাকি ইনপুটের জন্য form-control
            existing_classes = field.widget.attrs.get('class', '')
            if isinstance(field.widget, forms.Select):
                new_class = f"{existing_classes} form-select".strip()
            else:
                new_class = f"{existing_classes} form-control".strip()

            field.widget.attrs['class'] = new_class




from django.core.exceptions import ValidationError

class OTPRegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'আপনার পূর্ণ নাম'})
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '০১XXXXXXXXX'})
    )
    # 🟢 নতুন পাসওয়ার্ড ফিল্ড
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'পাসওয়ার্ড দিন'})
    )
    # 🟢 নতুন কনফার্ম পাসওয়ার্ড ফিল্ড
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'আবার পাসওয়ার্ড দিন'})
    )

    # দুটি পাসওয়ার্ড টাইপ করার সময় মিলল কিনা তা চেক করার ব্যাক-এন্ড ভ্যালিডেশন
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError({"confirm_password": "পাসওয়ার্ড দুটি ম্যাচ করেনি!"})
        return cleaned_data
