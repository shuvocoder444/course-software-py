from django import forms
from .models import Visitor, VisitorCategory

class VisitorCategoryForm(forms.ModelForm):
    class Meta:
        model = VisitorCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Admission, Official, Personal'}),
        }

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'mobile_number', 'purpose_category', 'visiting_date', 'additional_notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'purpose_category': forms.Select(attrs={'class': 'form-select'}), # বুটস্ট্র্যাপ ড্রপডাউন
            'visiting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Additional Notes ...'}),
        }
