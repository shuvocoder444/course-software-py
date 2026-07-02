

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
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.website_name
