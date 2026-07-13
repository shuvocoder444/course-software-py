from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

# আপনার কাস্টম লেআউট ও সিকিউরিটি মিক্সিন
from apps.account.views import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin
from apps.courses.models import Batch, Course
from apps.students.models import Student
from web_project import TemplateHelper

from .forms import InvoiceForm

# মডেল ইম্পোর্ট (শুধু যেগুলো নিশ্চিতভাবে আছে)
from .models import Invoice, StudentLedger

from django.db.models import Q
from apps.finance.models import Invoice
# আপনার প্রজেক্টের পাথ অনুযায়ী ইমপোর্ট নিশ্চিত করুন
# from apps.students.models import Batch, Course
# আপনার অন্যান্য মডেল এবং মিক্সিন ইমপোর্ট নিশ্চিত করুন
# from .models import Invoice, Batch, Course

class InvoiceListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Invoice
    context_object_name = 'invoices'
    template_name = 'invoice_list.html'
    ordering = ['-id']

    def get_queryset(self):
        # 💡 পারফরম্যান্স ফিক্স: select_related ব্যবহার করা হলো যাতে স্টুডেন্ট ও কোর্সের
        # ডেটা এক কুয়েরিতেই চলে আসে এবং লুপের ভেতর কোনো ডেটা মিস না হয়।
        queryset = Invoice.objects.select_related('student', 'student__course').all().order_by('-id')

        # URL এর GET রিকোয়েস্ট থেকে ফিল্টার ভ্যালু নেওয়া
        search_student = self.request.GET.get('search_student')  # 👈 নতুন যুক্ত করা হয়েছে
        batch_id = self.request.GET.get('batch')
        course_id = self.request.GET.get('course')
        session_id = self.request.GET.get('session')
        fee_type = self.request.GET.get('fee_type')

        # 🔍 স্টুডেন্ট নাম অথবা স্টুডেন্ট আইডি দিয়ে সার্চ ফিল্টারিং (নতুন যুক্ত)
        if search_student:
            queryset = queryset.filter(
                Q(student__name__icontains=search_student) |
                Q(student__student_id__icontains=search_student)
            )

        # স্টুডেন্টের রিলেশন ধরে ফিল্টারিং
        if batch_id:
            queryset = queryset.filter(student__batch_id=batch_id)
        if course_id:
            queryset = queryset.filter(student__course_id=course_id)
        if session_id:
            queryset = queryset.filter(student__session_id=session_id)

        # 👉 ফিক্স: ফর্ম ও মডেলের প্রকৃত ফিল্ডের নাম অনুযায়ী কন্ডিশন চেক
        if fee_type:
            if fee_type == 'course_fee':
                queryset = queryset.filter(course_fee__gt=0)
            elif fee_type == 'cert_fee':
                # যদি মডেলে certificate_fee থাকে তবে সেটি লিখুন, নতুবা cert_fee রাখুন
                if hasattr(Invoice, 'certificate_fee'):
                    queryset = queryset.filter(certificate_fee__gt=0)
                else:
                    queryset = queryset.filter(cert_fee__gt=0)
            elif fee_type == 'id_card_fee':
                queryset = queryset.filter(id_card_fee__gt=0)
            elif fee_type == 'admit_fee':
                # যদি মডেলে admit_card_fee থাকে তবে সেটি লিখুন
                if hasattr(Invoice, 'admit_card_fee'):
                    queryset = queryset.filter(admit_card_fee__gt=0)
                else:
                    queryset = queryset.filter(admit_fee__gt=0)
            elif fee_type == 'other_fee':
                queryset = queryset.filter(other_fee__gt=0)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ড্রপডাউন ডেটা পাঠানো হচ্ছে
        context['filter_data'] = {
            'batches': Batch.objects.all(),
            'courses': Course.objects.all(),
        }

        context['title'] = "Student Invoice List"
        return context




from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

# আপনার অ্যাপ অনুযায়ী প্রয়োজনীয় মডেল ও ফর্ম ইমপোর্ট রাখুন
# from .models import Invoice, StudentLedger, Student
# from .forms import InvoiceForm

# class InvoiceCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
#     model = Invoice
#     form_class = InvoiceForm
#     template_name = 'add_payment.html'
#     success_url = reverse_lazy('invoice_list')

#     def post(self, request, *args, **kwargs):
#         """
#         কাস্টম ড্রপডাউন থেকে টাইপ/সিলেক্ট করা আইডিকে Django ফর্মে
#         বাধ্যতামূলকভাবে অ্যাসাইন করার জন্য POST রিকোয়েস্ট ওভাররাইড করা হলো।
#         """
#         # রিকোয়েস্ট কপি করে এডিটেবল করা
#         post_data = request.POST.copy()

#         # ফ্রন্টএন্ডের কাস্টম সার্চ ইনপুট থেকে আইডিটি নেওয়া
#         custom_student_id = request.POST.get('student_search_input', '').strip()

#         # যদি মেইন স্টুডেন্ট ফিল্ড খালি থাকে কিন্তু কাস্টম সার্চ ইনপুটে আইডি থাকে, তবে মেইন ফিল্ডে তা বসানো
#         if not post_data.get('student') and custom_student_id:
#             post_data['student'] = custom_student_id

#         request.POST = post_data
#         return super().post(request, *args, **kwargs)

#     def form_valid(self, form):
#         with transaction.atomic():
#             invoice_instance = form.save(commit=False)
#             student = invoice_instance.student

#             # ১. চেক করা হচ্ছে এই স্টুডেন্টের কোনো ইনভয়েস আগে থেকে আছে কিনা
#             existing_invoice = Invoice.objects.filter(student=student).first()

#             new_payment = invoice_instance.paid_amount or Decimal('0.00')
#             new_discount = invoice_instance.discount or Decimal('0.00')

#             if existing_invoice:
#                 # ২. আগের ইনভয়েস থাকলে সেটি আপডেট হবে
#                 existing_invoice.course_fee = invoice_instance.course_fee
#                 existing_invoice.certificate_fee = invoice_instance.certificate_fee
#                 existing_invoice.id_card_fee = invoice_instance.id_card_fee
#                 existing_invoice.admit_card_fee = invoice_instance.admit_card_fee
#                 existing_invoice.other_fee = invoice_instance.other_fee

#                 existing_invoice.paid_amount += new_payment
#                 existing_invoice.discount = new_discount

#                 # পেমেন্ট মেথড আপডেট (HTML এ কাস্টম সিলেক্ট নেওয়া হয়েছিল)
#                 custom_pm = self.request.POST.get('payment_method')
#                 if custom_pm:
#                     existing_invoice.payment_method = custom_pm
#                 elif hasattr(invoice_instance, 'payment_method'):
#                     existing_invoice.payment_method = invoice_instance.payment_method

#                 existing_invoice.additional_notes = invoice_instance.additional_notes
#                 existing_invoice.save()

#                 active_invoice = existing_invoice
#                 description_text = f"Additional Payment Received ({active_invoice.invoice_no})"
#             else:
#                 # ৩. ইনভয়েস না থাকলে একদম নতুন ইনভয়েস তৈরি হবে
#                 current_time = datetime.now()
#                 invoice_instance.invoice_no = f"INV-{current_time.strftime('%Y%m%d-%H%M%S')}"

#                 # পেমেন্ট মেথড অ্যাসাইন
#                 custom_pm = self.request.POST.get('payment_method')
#                 if custom_pm:
#                     invoice_instance.payment_method = custom_pm

#                 invoice_instance.save()

#                 active_invoice = invoice_instance
#                 description_text = f"Fees Charged & Initial Payment Received ({active_invoice.invoice_no})"

#             # ৪. স্টুডেন্টের লেজার ব্যালেন্স ক্যালকুলেশন
#             last_ledger = StudentLedger.objects.filter(student=student).last()
#             previous_balance = last_ledger.balance if last_ledger else Decimal('0.00')

#             if existing_invoice:
#                 debit_amount = Decimal('0.00')
#                 credit_amount = new_payment
#                 current_balance = previous_balance - new_payment
#             else:
#                 debit_amount = active_invoice.net_payable if hasattr(active_invoice, 'net_payable') else Decimal('0.00')
#                 credit_amount = active_invoice.paid_amount
#                 current_balance = previous_balance + debit_amount - credit_amount

#             # লেজার রেকর্ড তৈরি
#             StudentLedger.objects.create(
#                 student=student,
#                 date=active_invoice.date,
#                 description=description_text,
#                 invoice=active_invoice,
#                 debit=debit_amount,
#                 credit=credit_amount,
#                 balance=current_balance
#             )

#             messages.success(self.request, f"Payment process successfully completed for {active_invoice.invoice_no}!")

#             # NoneType এরর ফিক্স করার মেইন পার্ট
#             self.object = active_invoice
#             return HttpResponseRedirect(self.get_success_url())







from apps.finance.models import Invoice, StudentLedger
# মিক্সিন এবং ফর্মের ইমপোর্ট নিশ্চিত করে নেবেন

class InvoiceCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'add_payment.html'
    success_url = reverse_lazy('invoice_list')

    def post(self, request, *args, **kwargs):
        """
        কাস্টম ড্রপডাউন থেকে টাইপ/সিলেক্ট করা আইডিকে Django ফর্মে
        বাধ্যতামূলকভাবে অ্যাসাইন করার জন্য POST রিকোয়েস্ট ওভাররাইড করা হলো।
        """
        post_data = request.POST.copy()
        custom_student_id = request.POST.get('student_search_input', '').strip()

        if not post_data.get('student') and custom_student_id:
            post_data['student'] = custom_student_id

        request.POST = post_data
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            invoice_instance = form.save(commit=False)
            student = invoice_instance.student

            # 💡 ফিক্স: আগের ইনভয়েস খোঁজার বা আপডেট করার কোনো লজিক থাকবে না।
            # প্রতিবার পেমেন্টে সরাসরি একদম নতুন ইনভয়েস তৈরি হবে।
            current_time = datetime.now()
            invoice_instance.invoice_no = f"INV-{current_time.strftime('%Y%m%d-%H%M%S')}"

            # পেমেন্ট মেথড অ্যাসাইন
            custom_pm = self.request.POST.get('payment_method')
            if custom_pm:
                invoice_instance.payment_method = custom_pm

            # নতুন ইনভয়েস ডেটাবেজে সেভ করা হলো
            invoice_instance.save()
            active_invoice = invoice_instance

            # ডিসক্রিপশন টেক্সট
            description_text = f"Payment Received ({active_invoice.invoice_no})"

            # 🎯 স্টুডেন্টের লেজার ব্যালেন্স ক্যালকুলেশন (১০০% আপনার লজিক অনুযায়ী)
            # আগের সর্বশেষ লেজার রেকর্ড খুঁজে বের করা
            last_ledger = StudentLedger.objects.filter(student=student).last()
            previous_balance = last_ledger.balance if last_ledger else Decimal('0.00')

            # প্রতিটা নতুন ইনভয়েসের জন্য ডেবিট, ক্রেডিট এবং কারেন্ট ব্যালেন্স হিসাব
            debit_amount = active_invoice.net_payable if hasattr(active_invoice, 'net_payable') else Decimal('0.00')
            credit_amount = active_invoice.paid_amount or Decimal('0.00')

            # নতুন ব্যালেন্স = পূর্বের ব্যালেন্স + নতুন চার্জ (Debit) - নতুন পেমেন্ট (Credit)
            current_balance = previous_balance + debit_amount - credit_amount

            # লেজার রেকর্ড তৈরি
            StudentLedger.objects.create(
                student=student,
                date=active_invoice.date,
                description=description_text,
                invoice=active_invoice,
                debit=debit_amount,
                credit=credit_amount,
                balance=current_balance
            )

            messages.success(self.request, f"Payment process successfully completed for {active_invoice.invoice_no}!")

            # NoneType এরর ফিক্স করার মেইন পার্ট
            self.object = active_invoice
            return HttpResponseRedirect(self.get_success_url())




# ৩. STUDENT LEDGER / STATEMENT VIEW
class StudentLedgerView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = StudentLedger
    context_object_name = 'ledger_entries'
    template_name = 'student_ledger.html'

    def get_queryset(self):
        self.student_instance = get_object_or_404(Student, pk=self.kwargs['pk'])
        return StudentLedger.objects.filter(student=self.student_instance).order_by('date', 'id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.student_instance

        queryset = self.get_queryset()
        context['total_charged'] = sum(item.debit for item in queryset)
        context['total_paid'] = sum(item.credit for item in queryset)

        last_entry = queryset.last()
        context['current_due'] = last_entry.balance if last_entry else Decimal('0.00')
        return context






from django.views.generic import DeleteView, DetailView, UpdateView

from .models import Invoice, StudentLedger


# ১. ইনভয়েস এডিট ভিউ (UpdateView)
class InvoiceUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'add_payment.html' # ক্রিয়েট আর এডিট একই ফর্মে হবে
    success_url = reverse_lazy('invoice_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Invoice"
        return context

    def form_valid(self, form):
        with transaction.atomic():
            invoice = form.save()
            # লেজারের ডেটা আপডেট করার কাস্টম কোড (প্রয়োজন হলে) এখানে লিখতে পারেন
            messages.success(self.request, f"Invoice {invoice.invoice_no} updated successfully!")
            return super().form_valid(form)


# ২. ইনভয়েস ডিলিট ভিউ (DeleteView)
class InvoiceDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice_list')

    # GET রিকোয়েস্টেই যেন ডিলিট হয়ে যায় (যেহেতু আমরা অ্যালার্ট দিয়ে কনফার্ম করছি)
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        with transaction.atomic():
            # এই ইনভয়েসের সাথে যুক্ত সব লেজার ডিলিট করা হচ্ছে
            StudentLedger.objects.filter(invoice=self.object).delete()
            # ইনভয়েস ডিলিট
            self.object.delete()

            messages.error(request, "Invoice and its related ledger records have been deleted!")
        return redirect(self.get_success_url())



class InvoicePrintView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoice_print.html'  # আগে শুধু 'invoice_print.html' ছিল
    context_object_name = 'invoice'




from django.http import JsonResponse
from .models import Invoice

def get_student_payment_details(request):
    student_id = request.GET.get('student_id')
    data = {
        'exists': False,
        'name': '',
        'phone': '',
        'course_name': '',
        'total_paid': 0,
        'discount': 0,
        'course_fee': 0,
        'certificate_fee': 0,
        'id_card_fee': 0,
        'admit_card_fee': 0,
        'other_fee': 0,
    }

    if student_id:
        print(f"\n[DEBUG] Fetching data for Student ID: {student_id}")

        invoice = Invoice.objects.filter(student_id=student_id)\
                                 .select_related('student__account', 'student__course')\
                                 .first()

        if invoice and invoice.student:
            student = invoice.student

            # ১. শিক্ষার্থীর নাম বের করা
            student_name = ""
            if student.account:
                student_name = student.account.get_full_name() or student.account.username

            # ২. শিক্ষার্থীর ফোন নম্বর বের করা
            student_phone = ""
            if student.account and hasattr(student.account, 'phone'):
                student_phone = student.account.phone
            elif hasattr(student, 'phone'):
                student_phone = student.phone

            # ৩. কোর্সের নাম বের করা
            course_title = ""
            if student.course:
                course_title = getattr(student.course, 'title', getattr(student.course, 'name', ''))

            # ৪. 👑 কোর্স ফি নির্ধারণ (ইনভয়েসে না থাকলে Course মডেলের default_fee থেকে আসবে)
            db_course_fee = float(invoice.course_fee or 0)

            if db_course_fee == 0 and student.course:
                # আপনার মডেলে থাকা default_fee ফিল্ডটি এখানে সরাসরি কল করা হয়েছে
                db_course_fee = float(student.course.default_fee or 0)
                print(f"[DEBUG] Invoice course_fee was 0. Pulled from Course Model (default_fee): {db_course_fee}")

            data = {
                'exists': True,
                'name': student_name,
                'phone': student_phone,
                'course_name': course_title,
                'course_fee': db_course_fee, # একদম সঠিক কোর্স ফি সেট হলো

                # অন্যান্য ফি ও হিসাব
                'total_paid': float(invoice.paid_amount or 0),
                'discount': float(invoice.discount or 0),
                'certificate_fee': float(invoice.certificate_fee or 0),
                'id_card_fee': float(invoice.id_card_fee or 0),
                'admit_card_fee': float(invoice.admit_card_fee or 0),
                'other_fee': float(invoice.other_fee or 0),
            }

            print(f"[DEBUG] Final Sending Data to Frontend: {data}\n")

    return JsonResponse(data)


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from .models import CompanyDeposit  # মডেল চেক করে নিন

# --- LIST VIEW WITH FILTERS & PAGINATION ---
class DepositListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = CompanyDeposit
    template_name = 'deposit_list.html'
    context_object_name = 'deposits'
    paginate_by = 10  # প্রতি পেজে ১০টি রেকর্ড থাকবে

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date')

        # গেট রিকোয়েস্ট থেকে প্যারামিটার রিসিভ করা
        search_query = self.request.GET.get('search')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # সার্চ ফিল্টারিং লজিক
        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(description__icontains=search_query)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset



# --- ADD / CREATE VIEW ---
class DepositCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, CreateView):
    model = CompanyDeposit
    fields = ['date', 'title', 'amount', 'file', 'description']
    success_url = reverse_lazy('deposit_list')

    def form_valid(self, form):
        messages.success(self.request, "Deposit added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add deposit. Please check the fields.")
        return redirect('deposit_list')





from django.views import View
from .models import CompanyDeposit

# --- FIX: MODAL BASED UPDATE VIEW ---
class DepositUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # আইডি অনুযায়ী অবজেক্ট খুঁজে বের করা
        deposit = get_object_or_404(CompanyDeposit, pk=pk)

        # মডাল ফর্ম থেকে পাঠানো ডেটা রিসিভ করা
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        date_val = request.POST.get('date')
        description = request.POST.get('description')

        # ফাইল আপলোড হ্যান্ডেল করা (যদি নতুন ফাইল দেওয়া হয়)
        if request.FILES.get('file'):
            deposit.file = request.FILES.get('file')

        # ডেটা ভ্যালিডেশন এবং আপডেট
        if title and amount and date_val:
            deposit.title = title
            deposit.amount = amount
            deposit.date = date_val
            deposit.description = description
            deposit.save() # ডাটাবেসে সেভ করা

            messages.success(request, "Deposit updated successfully!")
        else:
            messages.error(request, "Failed to update deposit. Invalid data.")

        return redirect('deposit_list')




from django.views import View
from .models import CompanyDeposit

# --- NEW & FIXED DELETE VIEW ---
class DepositDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        # আইডি অনুযায়ী অবজেক্টটি খুঁজে বের করবে
        deposit = get_object_or_404(CompanyDeposit, pk=pk)

        # অবজেক্টটি ডিলিট করবে
        deposit.delete()

        # মেসেজ দেখাবে
        messages.warning(request, "Deposit record deleted successfully!")

        # ডিলিট হওয়ার পর আবার লিস্ট পেজে ব্যাক করবে
        return redirect('deposit_list')









# Expense
# ==========================================
# ১. EXPENSE VIEWS (খরচ ব্যবস্থাপনা)
# ==========================================
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils.timezone import now
from django.views.generic import ListView, View

from web_project.template_helpers.theme import TemplateHelper

from .forms import ExpenseCategoryForm, ExpenseForm
from .models import Expense, ExpenseCategory


class ExpenseView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Expense
    context_object_name = "expenses"
    template_name = "expense/expense_list.html"
    paginate_by = 50  # ব্যাকএন্ডেও ডিফল্ট ৫০ করা হলো

    def get_queryset(self):
        self.search_query = self.request.GET.get("search", "").strip()
        self.category_filter = self.request.GET.get("category", "")
        self.start_date = self.request.GET.get("start_date", "")
        self.end_date = self.request.GET.get("end_date", "")

        queryset = Expense.objects.select_related("exp_category").order_by("-date")

        if self.search_query:
            queryset = queryset.filter(
                Q(exp_name__icontains=self.search_query) |
                Q(note__icontains=self.search_query) |
                Q(exp_category__name__icontains=self.search_query)
            )
        if self.category_filter:
            queryset = queryset.filter(exp_category_id=self.category_filter)
        if self.start_date:
            queryset = queryset.filter(date__gte=self.start_date)
        if self.end_date:
            queryset = queryset.filter(date__lte=self.end_date)

        return queryset

    def get(self, request, *args, **kwargs):
        # 🟢 AJAX রিকোয়েস্ট (DataTables) হ্যান্ডেলার যা প্রপার কাউন্ট পাঠাবে
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'data' in request.path:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 50)) # ডিফল্ট ৫০ রিসিভ করবে

            # কাউন্ট হিসাবের জন্য কুয়েরি
            all_expenses = Expense.objects.all()
            total_records = all_expenses.count()

            filtered_queryset = self.get_queryset()
            filtered_records = filtered_queryset.count()

            # টোটাল অ্যামাউন্ট হিসাব
            total_amount = filtered_queryset.aggregate(total=Sum("amount"))["total"] or 0

            # পেজিনেশন (সার্ভার সাইড স্লাইসিং)
            paginated_queryset = filtered_queryset[start : start + length]

            data = []
            for index, exp in enumerate(paginated_queryset, start=start + 1):
                data.append({
                    "id": exp.id,
                    "sl": index,
                    "date": exp.date.strftime('%Y-%m-%d') if exp.date else '',
                    "exp_name": exp.exp_name or '',
                    "amount": float(exp.amount),
                    "category": exp.exp_category.name if exp.exp_category else 'N/A',
                    "note": exp.note or '',
                })

            # 🟢 DataTable এর জন্য প্রয়োজনীয় প্রপার স্ট্রাকচার
            return JsonResponse({
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": filtered_records,
                "data": data,
                "total_amount": float(total_amount),
            })

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        total_expense = queryset.aggregate(total=Sum("amount"))["total"] or 0
        context["total_amount"] = float(total_expense)

        context["form"] = ExpenseForm()
        context["categories"] = ExpenseCategory.objects.all()
        context["search_query"] = self.search_query
        context["category_filter"] = self.category_filter
        context["start_date"] = self.start_date
        context["end_date"] = self.end_date

        return context

    def post(self, request, *args, **kwargs):
        expense_id = kwargs.get("pk") or request.POST.get("expense_id")
        instance = get_object_or_404(Expense, pk=expense_id) if expense_id else None

        form = ExpenseForm(request.POST, instance=instance)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                if request.POST.get("amount"):
                    expense.amount = int(float(request.POST.get("amount")))
                expense.save()
                return JsonResponse({
                    "success": True,
                    "message": f"Expense {'updated' if instance else 'added'} successfully."
                })
            except Exception as e:
                return JsonResponse({"success": False, "message": f"Database Error: {str(e)}"}, status=500)

        return JsonResponse({"success": False, "errors": form.errors, "message": "Validation error."}, status=400)





class ExpenseDataAPIView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    """ ফ্রন্টএন্ড ডাটা-টেবিলের সার্ভার সাইড জেসন ডাটা প্রোভাইডার """
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "").strip()

        category = request.GET.get("category", "")
        start_date = request.GET.get("start_date", "")
        end_date = request.GET.get("end_date", "")

        queryset = Expense.objects.select_related("exp_category").order_by("-date")
        total_records = queryset.count()

        if search_value:
            queryset = queryset.filter(
                Q(exp_name__icontains=search_value) |
                Q(note__icontains=search_value) |
                Q(exp_category__name__icontains=search_value)
            )

        if category:
            queryset = queryset.filter(exp_category_id=category)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        filtered_records = queryset.count()
        total_amount = queryset.aggregate(total=Sum("amount"))["total"] or 0

        paginated_queryset = queryset[start : start + length]

        data = []
        for index, expense in enumerate(paginated_queryset, start=start + 1):
            data.append({
                "id": expense.id,
                "sl": index,
                "date": expense.date.strftime("%Y-%m-%d"),
                "category": expense.exp_category.name if expense.exp_category else "",
                "name": expense.exp_name,
                "amount": f"{expense.amount} ৳",
                "note": expense.note or "—",
            })

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": data,
            "total_amount": float(total_amount),
        })


class ExpenseDetailAjaxView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    """ এডিট মডালে নির্দিষ্ট একটি খরচের ডাটা লোড করার ভিউ """
    def get(self, request, pk, *args, **kwargs):
        try:
            expense = Expense.objects.select_related("exp_category").get(pk=pk)
            return JsonResponse({
                "success": True,
                "expense": {
                    "id": expense.id,
                    "name": expense.exp_name,
                    "amount": str(expense.amount),
                    "date": expense.date.strftime("%Y-%m-%d"),
                    "note": expense.note or "",
                    "category_id": expense.exp_category.id if expense.exp_category else None,
                },
            })
        except Expense.DoesNotExist:
            return JsonResponse({"success": False, "message": "Expense not found."}, status=404)


class ExpenseDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return JsonResponse({"success": True, "message": "Expense deleted successfully."})


# ==========================================
# ২. EXPENSE CATEGORY VIEWS (ক্যাটাগরি ব্যবস্থাপনা)
# ==========================================

class ExpenseCategoryView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = ExpenseCategory
    context_object_name = "categories"
    template_name = "expense/expense_category_list.html"
    paginate_by = 10

    def get_queryset(self):
        self.search_query = self.request.GET.get("search", "").strip()
        queryset = ExpenseCategory.objects.all().order_by("-created_at")

        if self.search_query:
            queryset = queryset.filter(name__icontains=self.search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        context["form"] = ExpenseCategoryForm()
        context["search_query"] = self.search_query
        return context

    def post(self, request, *args, **kwargs):
        """ ক্যাটাগরি নরমাল সাবমিশন ও রিডাইরেক্ট হ্যান্ডেলার """
        category_id = kwargs.get("pk") or request.POST.get("id")
        instance = get_object_or_404(ExpenseCategory, pk=category_id) if category_id else None

        form = ExpenseCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Expense category {'updated' if instance else 'created'} successfully.")
        else:
            messages.error(request, "Failed to save category.")

        return redirect("expense_category_list")


class ExpenseCategoryAjaxView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    """ ক্যাটাগরি অ্যাসিনক্রোনাস (Ajax) সেভ করার ডেডিকেটেড ভিউ """
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get("id", "").strip()
        instance = None
        if category_id.isdigit():
            instance = ExpenseCategory.objects.filter(pk=int(category_id)).first()

        form = ExpenseCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            category = form.save()
            return JsonResponse({
                "success": True,
                "id": category.id,
                "name": category.name,
                "message": f"Category {'updated' if instance else 'created'} successfully.",
            })

        return JsonResponse({"success": False, "errors": form.errors, "message": "Validation failed."}, status=400)


class ExpenseCategoryDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(ExpenseCategory, pk=pk)
        category.delete()
        return JsonResponse({"success": True, "message": "Expense category deleted."})


# ==========================================
# ৩. PDF EXPORT (পিডিএফ রিপোর্ট জেনারেশন)
# ==========================================

def expense_export_pdf(request):
    search = request.GET.get("search", "").strip()
    category = request.GET.get("category", "").strip()
    start_date = request.GET.get("start_date", "").strip()
    end_date = request.GET.get("end_date", "").strip()

    expenses = Expense.objects.select_related("exp_category").order_by("date")

    if search:
        expenses = expenses.filter(
            Q(exp_name__icontains=search) | Q(note__icontains=search) | Q(exp_category__name__icontains=search)
        )
    if category:
        expenses = expenses.filter(exp_category_id=category)
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    total_expense = sum(e.amount for e in expenses)

    context = {
        "expenses": expenses,
        "total_expense": total_expense,
        "start_date": start_date,
        "end_date": end_date,
        "now": now(),
    }

    return render(request, "expense/expense_list_pdf.html", context)






from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# আপনার প্রজেক্টের সঠিক মিক্সিন পাথ অনুযায়ী এগুলো ইম্পোর্ট নিশ্চিত করুন
# from .mixins import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin
from .models import CompanyDeposit, Expense, Invoice

from django.contrib.auth.mixins import LoginRequiredMixin

# আপনার প্রজেক্টের সঠিক মিক্সিন ও মডেল পাথ অনুযায়ী এগুলো নিশ্চিত করুন
# from .mixins import AdminRoleRequiredMixin, VuxyVerticalLayoutMixin
from .models import CompanyDeposit, Expense, Invoice


class GeneralLedgerView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, TemplateView):
    template_name = 'general_ledger.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ১. ফিল্টার থেকে ডেট রিসিভ করা
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        today = date.today()

        # ডিফল্ট ফিল্টার: চলতি বছরের ১ জানুয়ারি থেকে আজকের দিন পর্যন্ত (যেন জুনের ডেটাও অটো দেখায়)
        start_date = datetime(today.year, 1, 1).date()
        end_date = today

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        context['start_date'] = start_date
        context['end_date'] = end_date

        # ২. ডাটাবেজ ফিল্টারিং (অপ্টিমাইজড কুয়েরি)
        invoices = Invoice.objects.filter(date__range=[start_date, end_date], paid_amount__gt=0).select_related('student')
        deposits = CompanyDeposit.objects.filter(date__range=[start_date, end_date])
        expenses = Expense.objects.filter(date__range=[start_date, end_date]).select_related('exp_category')

        # ৩. ইনকাম সাইডের ডেটা কম্বাইন করা (Invoice + Deposit)
        income_list = []
        for inv in invoices:
            income_list.append({
                'date': inv.date,
                'particulars': f"{inv.invoice_no} ({inv.student.name if inv.student else 'Student'})",
                'amount': float(inv.paid_amount)
            })
        for dep in deposits:
            income_list.append({
                'date': dep.date,
                'particulars': f"{dep.title} (Deposit)",
                'amount': float(dep.amount)
            })

        # ৪. এক্সপেন্স সাইডের ডেটা লেজার ফরম্যাটে তৈরি করা
        expense_list = []
        for exp in expenses:
            category_name = exp.exp_category.name if exp.exp_category else "General"
            expense_list.append({
                'date': exp.date,
                'particulars': f"{exp.exp_name} ({category_name})",
                'amount': float(exp.amount),
                'note': exp.note or ""
            })

        # তারিখ অনুযায়ী সর্টিং (নতুন ডাটা উপরে থাকবে)
        income_list = sorted(income_list, key=lambda x: x['date'], reverse=True)
        expense_list = sorted(expense_list, key=lambda x: x['date'], reverse=True)

        # ৫. সামারি কার্ডের জন্য ক্যালকুলেশন
        total_invoice_income = invoices.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        total_deposit_income = deposits.aggregate(Sum('amount'))['amount__sum'] or 0
        total_income = float(total_invoice_income) + float(total_deposit_income)

        total_expense = float(expenses.aggregate(Sum('amount'))['amount__sum'] or 0)
        net_balance = total_income - total_expense

        # ৬. টেমপ্লেটে ডাটা পাঠানো
        context['incomes'] = income_list
        context['expenses'] = expense_list
        context['total_income'] = total_income
        context['total_expense'] = total_expense
        context['net_balance'] = net_balance

        return context



from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# আপনার স্টুডেন্ট মডেলটি ইমপোর্ট করুন
# from .models import Student

class StudentSearchAjaxView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        results = []

        # 🔍 DEBUG: রিকোয়েস্ট আসছে কিনা এবং কি কোয়েরি আসছে তা টার্মিনালে দেখাবে
        print("\n[DEBUG] --- Student Search AJAX Called ---")
        print(f"[DEBUG] Search Query Received: '{query}'")

        if query:
            students = Student.objects.filter(
                Q(student_id__icontains=query) | Q(name__icontains=query)
            )

            # 🔍 DEBUG: ডাটাবেজ থেকে কয়টি রেকর্ড ম্যাচ করলো
            print(f"[DEBUG] Total Students Found in DB: {students.count()}")

            for student in students:
                results.append({
                    'id': student.id,           # ডাটাবেজের প্রাইমারি কী (PK)
                    'student_id': student.student_id, # যেমন: 780
                    'name': student.name,       # যেমন: Md Maruf hossen
                })
        else:
            print("[DEBUG] Warning: Empty query received.")

        # 🔍 DEBUG: ফাইনাল রেসপন্স ডেটা টার্মিনালে প্রিন্ট করে দেখা
        print(f"[DEBUG] JSON Response Data: {results}\n")

        return JsonResponse({'students': results})




from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.finance.models import Invoice  # আপনার ইনভয়েস মডেলের সঠিক ইম্পোর্ট পাথ

def search_student_ajax(request):
    """
    ১. ইনপুট বক্সে আইডি (যেমন: 780) বা নাম টাইপ করলে ড্রপডাউন সাজেশন দেখানোর ভিউ
    """
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        # student_id অথবা name ফিল্ডের সাথে মিলিয়ে টপ ১০ জন স্টুডেন্ট খোঁজা
        students = Student.objects.filter(
            Q(student_id__icontains=query) | Q(name__icontains=query)
        )

        for student in students:
            results.append({
                'id': student.id,                 # ডাটাবেজের অটো-ইনক্রিমেন্ট ID (PK)
                'student_id': student.student_id, # কাস্টম স্টুডেন্ট আইডি (যেমন: 780)
                'name': student.name,
            })

    return JsonResponse({'students': results})



from apps.finance.models import Invoice

def get_student_details_ajax(request):
    """
    শিক্ষার্থীর আইডি অনুযায়ী তার প্রোফাইল ও курс ফির ডিটেইলস স্বয়ংক্রিয়ভাবে রিটার্ন করার মাস্টার ভিউ
    """
    student_id = request.GET.get('student_id', '').strip()
    custom_id = request.GET.get('custom_id', '').strip()

    try:
        student = None

        # ১. প্রথমে ডাটাবেজের প্রাইমারি কি (PK/ID) দিয়ে খোঁজা
        if student_id and student_id.isdigit():
            student = Student.objects.filter(id=student_id).first()

        # ২. ব্যাকআপ হিসেবে শিক্ষার্থীর কাস্টম রোল/আইডি (student_id) দিয়ে খোঁজা
        if not student and custom_id:
            student = Student.objects.filter(student_id=custom_id).first()

        if not student:
            return JsonResponse({
                'exists': False,
                'error': f"Student not found for DB-ID: '{student_id}' or Custom-ID: '{custom_id}'"
            })

        course_name = ""
        course_fee = 0.00
        if student.course:
            course_name = getattr(student.course, 'name', '')
            course_fee = float(getattr(student.course, 'default_fee', 0.00))

        # ৪. পূর্বের ইনভয়েসগুলোর মোট পরিশোধিত টাকা (পারফেক্টলি আগের মতোই)
        total_paid = 0.00
        invoice_summary = Invoice.objects.filter(student=student).aggregate(total=Sum('paid_amount'))
        if invoice_summary['total'] is not None:
            total_paid = float(invoice_summary['total'])

        return JsonResponse({
            'exists': True,
            'name': student.name if student.name else "",
            'phone': student.phone if student.phone else "",
            'course_name': course_name,
            'course_fee': course_fee,
            'total_paid': total_paid
        })

    except Exception as e:
        return JsonResponse({
            'exists': False,
            'error': f"Internal Server Error: {str(e)}"
        })
