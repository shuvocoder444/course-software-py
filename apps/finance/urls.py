from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import (
    ExpenseCategoryAjaxView,
    ExpenseCategoryDeleteView,
    ExpenseCategoryView,
    ExpenseDeleteView,
    ExpenseDetailAjaxView,
    ExpenseView,
)

urlpatterns = [
    path('invoice/<int:pk>/edit/', views.InvoiceUpdateView.as_view(), name='invoice_edit'),
    path('invoice/<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoice/<int:pk>/print/', views.InvoicePrintView.as_view(), name='invoice_print'),
    path('invoice/list/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('payment/add/', views.InvoiceCreateView.as_view(), name='add_payment'),
    path('student/<int:pk>/ledger/', views.StudentLedgerView.as_view(), name='student_ledger'),

    # 🎯 ফিক্সড ও সিঙ্কড AJAX রাউটস (ফ্রন্টএন্ড স্ক্রিপ্টের সাথে মিল রেখে)
    path('ajax/search-student/', views.search_student_ajax, name='search_student_ajax'),
    path('ajax/get-student-details/', views.get_student_details_ajax, name='get_student_details_ajax'),

    path('ledger/', views.GeneralLedgerView.as_view(), name='general_ledger'),
    path('deposits/', views.DepositListView.as_view(), name='deposit_list'),
    path('deposits/add/', views.DepositCreateView.as_view(), name='deposit_add'),
    path('deposits/edit/<int:pk>/', views.DepositUpdateView.as_view(), name='deposit_edit'),
    path('deposits/delete/<int:pk>/', views.DepositDeleteView.as_view(), name='deposit_delete'),

    # Expense
    path("expenses/data/", login_required(ExpenseView.as_view()), name="expense_data"),
    path("expenses/data/<int:pk>/", login_required(ExpenseDetailAjaxView.as_view()), name="expense_detail_ajax"),
    path("expenses/", login_required(ExpenseView.as_view()), name="expense_list"),
    path("expenses/edit/<int:pk>/", login_required(ExpenseView.as_view()), name="edit_expense"),
    path("expenses/delete/<int:pk>", login_required(ExpenseDeleteView.as_view()), name="delete_expense"),

    # Expense Categories
    path("expense-categories/ajax/save/", login_required(ExpenseCategoryAjaxView.as_view()), name="ajax_expense_category_save"),
    path("expense-categories/", login_required(ExpenseCategoryView.as_view()), name="expense_category_list"),
    path("expense-categories/edit/<int:pk>/", login_required(ExpenseCategoryView.as_view()), name="edit_expense_category"),
    path("expense-categories/delete/<int:pk>/", login_required(ExpenseCategoryDeleteView.as_view()), name="delete_expense_category"),
    path("expenses/export-pdf/", login_required(views.expense_export_pdf), name="expense_export_pdf"),
]
