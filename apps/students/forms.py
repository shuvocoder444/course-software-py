from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__' # এখানে '__all__' না থাকলে ফর্মে কিছুই দেখাবে না
        # অথবা আপনি ফিল্ডের নাম এভাবে দিতে পারেন:
        # fields = ['account', 'student_id', 'name', 'email', 'phone', 'class_name', 'roll', 'status']
