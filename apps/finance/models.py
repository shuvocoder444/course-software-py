from datetime import date

from django.db import models

# ইনভয়েস স্ট্যাটাসের চয়েসসমূহ
STATUS_CHOICES = [
    ('Due', 'Due'),
    ('Partially Paid', 'Partially Paid'),
    ('Paid', 'Paid'),
]

class Invoice(models.Model):
    # স্ট্রিং রেফারেন্স ব্যবহার করে অন্য অ্যাপের মডেল কানেক্ট করা হলো
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='invoices')
    invoice_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    date = models.DateField(default=date.today)

    # ৪টি নির্দিষ্ট খাত এবং অন্যান্য ফি
    course_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    certificate_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    id_card_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    admit_card_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # সামারি হিসাব
    total_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_payable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Due')
    additional_notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # অটোমেটিক হিসাব-নিকাশ
        self.total_gross = self.course_fee + self.certificate_fee + self.id_card_fee + self.admit_card_fee + self.other_fee
        self.net_payable = self.total_gross - self.discount
        self.due_amount = self.net_payable - self.paid_amount

        # স্ট্যাটাস নির্ধারণ
        if self.paid_amount >= self.net_payable:
            self.status = 'Paid'
        elif self.paid_amount > 0:
            self.status = 'Partially Paid'
        else:
            self.status = 'Due'

        # ডেমো ইনভয়েস নম্বর জেনারেশন (যদি না থাকে)
        if not self.invoice_no:
            super().save(*args, **kwargs) # আইডি পাওয়ার জন্য প্রথমে একবার সেভ
            self.invoice_no = f"INV-{date.today().strftime('%Y%m%d')}-{self.id}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_no or 'Draft Invoice'} - {self.student}"


class StudentLedger(models.Model):
    # এখানেও সঠিক অ্যাপ লেবেল 'students.Student' ব্যবহার করা হয়েছে
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='ledger_records')
    date = models.DateField(default=date.today)
    description = models.CharField(max_length=255)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='ledger_entries')

    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # শিক্ষার্থীর বকেয়া/পাওনা বৃদ্ধি পেলে
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # শিক্ষার্থী টাকা পরিশোধ করলে
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.student} - {self.description}"



class CompanyDeposit(models.Model):
    date = models.DateField(default=date.today)
    title = models.CharField(max_length=255) # যেমন: Opening Balance, Partner Capital etc.
    category = models.CharField(max_length=100, default='Deposit') # ফিক্সড ক্যাটাগরি
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    file = models.FileField(upload_to='deposit_documents/', blank=True, null=True) # ডকুমেন্ট আপলোডের জন্য
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

# Expense Section
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Expense Type", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name






class Expense(models.Model):
    exp_category = models.ForeignKey(
        ExpenseCategory, on_delete=models.CASCADE, related_name="expenses", verbose_name="Expense Category"
    )
    exp_name = models.CharField(max_length=255, verbose_name="Expense Name", null=True, blank=True)
    date = models.DateField(verbose_name="Date")
    amount = models.IntegerField(verbose_name="Expense Amount")
    note = models.TextField(blank=True, null=True, verbose_name="Expense Note")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exp_name} - {self.amount} ৳"
