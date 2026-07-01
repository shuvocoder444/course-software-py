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
