# apps/account/models.py (👑 সম্পূর্ণ ক্লিন এবং ফিক্সড কোড)
from django.contrib.auth.models import AbstractUser
from django.db import models

class Account(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STUDENT = 'STUDENT', 'Student'
        ACCOUNTS = 'ACCOUNTS', 'Accounts'
        TEACHER = 'TEACHER', 'Teacher'
        RECEPTION = 'RECEPTION', 'Reception'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )

    def __str__(self):
        # 👑 ফিক্স: self.username যদি অবজেক্ট হিসেবে না আসে, তাই স্ট্রিং সেফ রাখা হলো
        return f"{self.username} ({self.role})"



from django.db import models
from django.utils import timezone
import datetime



from django.db import models

class SMSVerification(models.Model):
    """মোবাইল নম্বর ভেরিফিকেশনের জন্য ওটিপি ট্র্যাকিং মডেল"""
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="মোবাইল নম্বর"
    )
    otp_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        verbose_name="ওটিপি কোড"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name="তৈরির সময়"
    )
    is_used = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="ব্যবহার করা হয়েছে?"
    )

    class Meta:
        verbose_name = "SMS ভেরিফিকেশন"
        verbose_name_plural = "SMS ভেরিফিকেশনসমূহ"
        ordering = ['-created_at']

    def is_valid(self):
        """ওটিপি কোডটি ৫ মিনিটের জন্য সচল বা ভ্যালিড থাকবে"""
        if not self.created_at:
            return False
        time_difference = timezone.now() - self.created_at
        return not self.is_used and time_difference < datetime.timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone_number} - {self.otp_code} ({'ব্যব্যহৃত' if self.is_used else 'সক্রিয়'})"
