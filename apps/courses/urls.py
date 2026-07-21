from django.urls import path
from . import views  # 👈 এভাবে সরাসরি views ইম্পোর্ট করা সবচেয়ে সেফ

urlpatterns = [
    # --- Course URLs ---
    path('', views.CourseListView.as_view(), name='course_list'), # 👈 এখানে CourseView এর বদলে CourseListView হবে
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/edit/', views.CourseEditView.as_view(), name='course_edit'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # --- Batch URLs ---
    path('batches/', views.BatchListView.as_view(), name='batch_list'),
    path('batches/create/', views.BatchCreateView.as_view(), name='batch_create'),
    path('batches/<int:pk>/edit/', views.BatchEditView.as_view(), name='batch_edit'),
    path('batches/<int:pk>/delete/', views.BatchDeleteView.as_view(), name='batch_delete'),


    # ...enrollments আপনার কোর্সের অন্যান্য ইউআরএল
path('admin/enrollments/', views.AdminEnrollmentDashboardView.as_view(), name='admin_enrollment_dashboard'),
    path('admin/enrollments/approve/<int:enrollment_id>/', views.AdminApproveEnrollmentView.as_view(), name='admin_approve_enrollment'),
    path('admin/enrollments/reject/<int:enrollment_id>/', views.AdminRejectEnrollmentView.as_view(), name='admin_reject_enrollment'),
]
