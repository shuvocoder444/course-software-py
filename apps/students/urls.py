from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student_list'),
    path('add/', views.StudentCreateView.as_view(), name='student_create'),
    path('edit/<int:pk>/', views.StudentEditView.as_view(), name='student_edit'),
    path('delete/<int:pk>/', views.StudentDeleteView.as_view(), name='student_delete'),

    # 🆕 নতুন যুক্ত করা পাথসমূহ (Approve এবং Print)
    path('approve/<int:pk>/', views.StudentApproveView.as_view(), name='student_approve'),
    path('print/<int:pk>/', views.StudentPrintView.as_view(), name='student_print'),

    # 👑 এই লাইনটি অবশ্যই চেক করুন
    path('ajax/load-batches/', views.LoadBatchesView.as_view(), name='ajax_load_batches'),
]
