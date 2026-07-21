from django import forms
from .models import Course, Batch

from apps.courses.models import Course # LEVEL_CHOICES ইম্পোর্ট করা না থাকলে করে নিবেন

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'name', 'code', 'default_fee', 'duration_months',
            'total_classes', 'total_hours', 'level', 'image', 'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course code'}),
            'default_fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3'}),
            'total_classes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 24'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 48'}),
            'level': forms.Select(attrs={'class': 'form-select'}), # ড্রপডাউনের জন্য form-select ব্যবহার করা হয়েছে
            'image': forms.FileInput(attrs={'class': 'form-control'}), # ইমেজ আপলোডের জন্য FileInput
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short details...'}),
        }
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['course', 'batch_number', 'start_date', 'is_active']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Batch-01'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
