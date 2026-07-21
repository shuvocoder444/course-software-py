from django.db import models



class AttendenceSetting(models.Model):
    website_name = models.CharField(max_length=255, default="My Institute Portal Layout", null=True, blank=True)
    send_id_token = models.CharField(max_length=255, null=True, blank=True)
    # send_id_token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)

    # রেজিস্ট্রেশন এসএমএস টেমপ্লেট
    reg_sms = models.TextField(
        null=True,
        blank=True,
        default="প্রিয় [name], JBD IT-তে আপনাকে স্বাগতম! পোর্টালে লগইন করতে ব্যবহার করুন Username: [phone] এবং Password: [phone]"
    )
    student_sms = models.TextField(
        null=True,
        blank=True,
        default="প্রিয় [name], JBD IT-তে আপনাকে স্বাগতম! পোর্টালে লগইন করতে ব্যবহার করুন Username: [phone] এবং Password: [phone]"
    )
    # স্টুডেন্ট অ্যাপ্রুভাল এসএমএস টেমপ্লেট
    approve_sms = models.TextField(blank=True, null=True, verbose_name="Student Approval Confirmation SMS")

    # 🎯 নতুন যুক্ত করা পেমেন্ট এসএমএস টেমপ্লেট
    payment_sms = models.TextField(
        null=True,
        blank=True,
        default="প্রিয় [name], আপনার পেমেন্ট সফলভাবে সম্পন্ন হয়েছে। রশিদ নং: [invoice], পরিশোধিত টাকা: [amount]/-। ধন্যবাদ!",
        verbose_name="Student Payment Confirmation SMS"
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.website_name or "Attendance Setting"



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





from django.db import models

class SiteSetting(models.Model):
   # --- Institution Information ---
    institution_name = models.CharField(max_length=250,blank=True, null=True, default="JBDIT")
    email = models.EmailField(max_length=105,blank=True, null=True, default="JBDIT@gmail.com")
    post_office = models.CharField(max_length=101,blank=True, null=True, default="JBDIT")
    upozila = models.CharField(max_length=100,blank=True, null=True, default="JBDIT")
    district = models.CharField(max_length=100,blank=True, null=True, default="Rajshahi")
    eiin = models.CharField(max_length=20, blank=True, null=True, )
    school_code = models.CharField(max_length=50, blank=True, null=True)
    established_at = models.CharField(max_length=10,blank=True, null=True, )
    phone_number = models.CharField(max_length=20,blank=True, null=True, )
    map_link = models.URLField(max_length=500,blank=True, null=True)

    # --- Weekend & Status ---
    # একাধিক দিন সিলেক্ট করার জন্য BooleanField ব্যবহার করা সবচেয়ে সেফ এবং UI বান্ধব
    friday = models.BooleanField(default=True, verbose_name="Friday")
    saturday = models.BooleanField(default=True, verbose_name="Saturday")
    sunday = models.BooleanField(default=False, verbose_name="Sunday")
    monday = models.BooleanField(default=False, verbose_name="Monday")
    tuesday = models.BooleanField(default=False, verbose_name="Tuesday")
    wednesday = models.BooleanField(default=False, verbose_name="Wednesday")
    thursday = models.BooleanField(default=False, verbose_name="Thursday")



    # --- Media Elements ---
    banner = models.ImageField(upload_to='site_settings/', blank=True, null=True)
    logo = models.ImageField(upload_to='site_settings/logo_fav/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site_settings/logo_fav/', blank=True, null=True)


# --- PDF Banners ---
    student_admission_pdf_banner = models.ImageField(upload_to="pdf/banners/", blank=True, null=True)
    invoice_pdf_banner = models.ImageField(upload_to="pdf/banners/", blank=True, null=True)

    def __str__(self):
        return self.institution_name

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
