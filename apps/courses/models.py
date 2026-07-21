from django.db import models
from django.utils.text import slugify
from django.conf import settings
LEVEL_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]
class Course(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Course Name")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Slug")
    code = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Course Code")
    default_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Course Fee")
    description = models.TextField(blank=True, null=True, verbose_name="Course Description")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, verbose_name="Course Image")
    duration_months = models.IntegerField(default=0, verbose_name="Duration (Months)")
    total_classes = models.IntegerField(default=0, verbose_name="Total Classes")
    total_hours = models.IntegerField(default=0, verbose_name="Total Hours")
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Beginner', verbose_name="Course Level")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # যদি স্ল্যাগ খালি থাকে এবং কোর্সের নাম দেওয়া থাকে
        if not self.slug and self.name:
            self.slug = slugify(self.name)

            # ডেটাবেসে একই স্ল্যাগ অলরেডি আছে কিনা তা চেক করার জন্য লুপ
            original_slug = self.slug
            counter = 1
            while Course.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else "Unnamed Course"







# --- এই দুটি মডেল নিচে বসিয়ে দিন ---

class Enrollment(models.Model):
    # 'apps.students.Student' ব্যবহার করে সরাসরি সঠিক পাথের মডেলকে পয়েন্ট করা হলো
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE,blank=True, null=True,  related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True, null=True,  related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.course.name}"

class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True, null=True, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name} ({self.rating}★)"








class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches', verbose_name="Select Course")
    batch_number = models.CharField(max_length=100, verbose_name="Batch Number/Name")
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __str__(self):
        return self.batch_number
