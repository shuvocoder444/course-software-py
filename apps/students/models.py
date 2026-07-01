from django.conf import settings
from django.db import models


class Student(models.Model):
    # 👑 চয়েস লিস্টগুলো ক্লাসের একদম শুরুতে ডিফাইন করা হলো
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    MARITAL_CHOICES = [('single', 'Single'), ('married', 'Married')]
    BLOOD_GROUPS = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')]
    RELIGION_CHOICES = [('islam', 'Islam'), ('hindu', 'Hinduism'), ('christian', 'Christianity'), ('buddhist', 'Buddhism'), ('others', 'Others')]

    # Relation (👑 সেটিংস থেকে কাস্টম ইউজার মডেল ট্র্যাক করবে)
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        null=True,
        blank=True
    )

    # 👑 Course এবং Batch এর সাথে রিলেশন যুক্ত করা হলো
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    batch = models.ForeignKey(
        'courses.Batch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    # 1. Student Basic Info
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    # Address Info
    village_house_area = models.CharField(max_length=255, blank=True, null=True)
    thana_upazila = models.CharField(max_length=100, blank=True, null=True)
    district_city = models.CharField(max_length=100, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)

    # Personal Info
    date_of_birth = models.DateField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_CHOICES, blank=True, null=True)
    birth_certificate_no = models.CharField(max_length=50, blank=True, null=True)
    national_id_no = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True, null=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS, blank=True, null=True)
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)

    # 2. Guardian Information
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_phone = models.CharField(max_length=15, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)

    # 3. Academic Information
    education_institute_name = models.CharField(max_length=255, blank=True, null=True)
    last_educational_qualification = models.CharField(max_length=100, blank=True, null=True)
    examination = models.CharField(max_length=50, blank=True, null=True)
    passing_year = models.IntegerField(blank=True, null=True)
    board_name = models.CharField(max_length=100, blank=True, null=True)
    roll = models.IntegerField(blank=True, null=True)
    registration_number = models.CharField(max_length=50, blank=True, null=True)

    # অটোমেটিক তৈরি হওয়ার জন্য ৩টি ফিল্ড (👑 সেশনের লেন্থ বাড়িয়ে ১০০ করা হলো)
    session = models.CharField(max_length=100, blank=True, null=True, help_text="Auto-generated full session timestamp")
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name
