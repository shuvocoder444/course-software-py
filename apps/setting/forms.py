# forms.py (আপনার অ্যাপ ফোল্ডারের ভেতর)
from django import forms

from .models import InstituteSetting


class InstituteSettingForm(forms.ModelForm):
    class Meta:
        model = InstituteSetting
        fields = '__all__'  # অথবা আপনি নির্দিষ্ট ফিল্ডের নাম দিতে পারেন যেমন: ['name', 'logo', 'address']

        # বুটস্ট্র্যাপ ডিজাইন সুন্দর করার জন্য ফর্ম উইজেট (ঐচ্ছিক)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # আপনার মডেলের অন্য ফিল্ডগুলো এখানে যুক্ত করতে পারেন
        }
