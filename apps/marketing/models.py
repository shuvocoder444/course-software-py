from django.db import models

# ১. ডাইনামিক ক্যাটাগরি মডেল
class VisitorCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ২. ভিজিটর মডেল
class Visitor(models.Model):
    name = models.CharField(max_length=255, verbose_name="Visitor's Name")
    mobile_number = models.CharField(max_length=20, verbose_name="Mobile Number")
    # এখানে স্ট্যাটিক চয়েসের বদলে ডাইনামিক ForeignKey ব্যবহার করা হয়েছে
    purpose_category = models.ForeignKey(VisitorCategory, on_delete=models.PROTECT, related_name='visitors', verbose_name="Visiting Purpose Category")
    visiting_date = models.DateField(verbose_name="Visiting Date")
    additional_notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.mobile_number}"
