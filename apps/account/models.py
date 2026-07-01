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
