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
        return f"{self.username} ({self.role})"
