from django import forms

from ..courses.models import Batch  # 👑 এখানে অ্যাড করা হলো (Relative Import)
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # পরিবর্তন ১: 'student_id' এখান থেকে বাদ দেওয়া হলো যাতে এটি ফর্মে শো করে
        exclude = ['account', 'status', 'session']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👑 ডাইনামিক ড্রপডাউন হ্যান্ডেল করার লজিক (কোর্স সিলেক্ট করলে সেই কোর্সের ব্যাচ আসবে)
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['batch'].queryset = Batch.objects.filter(course_id=course_id).order_by('batch_number')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.course:
            self.fields['batch'].queryset = self.instance.course.batches.order_by('batch_number')
        else:
            # প্রথমবার ফর্ম লোড হলে ব্যাচ খালি থাকবে (AJAX দিয়ে পরে লোড হবে)
            self.fields['batch'].queryset = Batch.objects.none()

        # প্লেসহোল্ডার ডিকশনারি (পরিবর্তন ২: 'student_id'-এর প্লেসহোল্ডার যুক্ত করা হলো)
        placeholders = {
            'student_id': 'e.g. STU-2026-0001',
            'name': 'Enter full name',
            'phone': '01XXXXXXXXX',
            'email': 'example@email.com',
            'course': '--- Select Course ---',
            'batch': '--- Select Batch ---',
            'village_house_area': 'Village or area name',
            'thana_upazila': 'Thana or Upazila',
            'district_city': 'District',
            'post_code': 'Post code',
            'birth_certificate_no': 'Certificate number',
            'national_id_no': 'NID number',
            'father_name': "Enter father's full name",
            'father_phone': "Father's mobile number",
            'father_occupation': "e.g. Farmer, Business",
            'mother_name': "Enter mother's full name",
            'guardian_name': 'If different from parents',
            'guardian_phone': "Guardian's mobile number",
            'education_institute_name': 'School / College / University name',
            'last_educational_qualification': 'e.g. SSC, HSC, Bachelor',
            'examination': 'e.g. SSC, HSC',
            'passing_year': 'e.g. 2023',
            'board_name': 'e.g. Dhaka, Rajshahi',
            'roll': 'Roll No.',
            'registration_number': 'Reg. Number',
        }

        # লুপের মাধ্যমে প্লেসহোল্ডার এবং বুটস্ট্র্যাপ/ভিউক্সি ক্লাস অ্যাসাইন
        for field_name, field in self.fields.items():
            if field_name in placeholders:
                if isinstance(field.widget, forms.Select):
                    field.empty_label = placeholders[field_name]
                else:
                    field.widget.attrs['placeholder'] = placeholders[field_name]

            existing_classes = field.widget.attrs.get('class', '')
            if isinstance(field.widget, forms.Select):
                new_class = f"{existing_classes} form-select".strip()
            else:
                new_class = f"{existing_classes} form-control".strip()

            field.widget.attrs['class'] = new_class

    # পরিবর্তন ৩: ইউনিক আইডি ভ্যালিডেশন (একই আইডি দুইবার দিলে এরর দেখাবে)
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')

        # যদি আমরা এক্সিস্টিং স্টুডেন্ট এডিট করি, তবে আইডি চেক স্কিপ করবে
        if self.instance.pk and self.instance.student_id == student_id:
            return student_id

        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("এই স্টুডেন্ট আইডিটি ইতিমধ্যে ব্যবহার করা হয়েছে! দয়া করে অন্য আইডি দিন।")
        return student_id
