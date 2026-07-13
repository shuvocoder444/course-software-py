from django import forms

from .models import Invoice
# E:\Course\apps\finance\forms.py

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice  # রিলেশন মডেলে থাকার কারণে এখানে শুধু মূল মডেলটিই থাকবে
        fields = [
            'student', 'date', 'course_fee', 'certificate_fee',
            'id_card_fee', 'admit_card_fee', 'other_fee',
            'discount', 'paid_amount', 'additional_notes'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control select2'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        money_fields = ['course_fee', 'certificate_fee', 'id_card_fee', 'admit_card_fee', 'other_fee', 'discount', 'paid_amount']
        for field in money_fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            if not self.initial.get(field):
                self.fields[field].initial = 0.00



# Expense
from .models import Expense, ExpenseCategory


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ["name"]


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["exp_category", "exp_name", "date", "amount", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
