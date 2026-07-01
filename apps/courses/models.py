from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Course Name")
    code = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Course Code")
    default_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Course Fee")
    description = models.TextField(blank=True, null=True, verbose_name="Course Description")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches', verbose_name="Select Course")
    batch_number = models.CharField(max_length=100, verbose_name="Batch Number/Name")
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __str__(self):
        return self.batch_number
