from django.db import models

class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    # 'account' অ্যাপের 'Account' মডেলের সাথে ওয়ান-টু-ওয়ান রিলেশন
    account = models.OneToOneField(
        'account.Account',
        on_delete=models.CASCADE,
        related_name='student_profile',
        null=True,
        blank=True
    )

    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    class_name = models.CharField(max_length=50)
    roll = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name
