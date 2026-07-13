from django.db import models


class AttendenceSetting(models.Model):
    website_name = models.CharField(max_length=255, default="My Institute Portal Layout", null=True, blank=True)
    send_id_token = models.CharField(max_length=255, null=True, blank=True)
    # send_id_token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
    reg_sms = models.TextField(
        null=True,
        blank=True,
        default="প্রিয় [name], JBD IT-তে আপনাকে স্বাগতম! পোর্টালে লগইন করতে ব্যবহার করুন Username: [phone] এবং Password: [phone]"
    )
    approve_sms = models.TextField(blank=True, null=True, verbose_name="Student Approval Confirmation SMS")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.website_name


# apps/setting/models.py (অথবা আপনার সুবিধাজনক কোনো অ্যাপের models.py তে)
from django.db import models

class SMSLog(models.Model):
    SMS_TYPES = [
        ('registration', 'Registration Welcome'),
        ('approval', 'Admission Approval'),
    ]

    student_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    sms_type = models.CharField(max_length=20, choices=SMS_TYPES, default='registration')
    status = models.CharField(max_length=20, default='success') # success, failed
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # নতুন এসএমএসগুলো সবার উপরে দেখাবে

    def __str__(self):
        return f"{self.student_name} - {self.phone} ({self.get_sms_type_display()})"
