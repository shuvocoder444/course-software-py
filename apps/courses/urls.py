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
]
