from django.urls import path
from . import views  # সব ভিউ ইমপোর্ট হলো

urlpatterns = [
    # Auth Routes
# ২. ফ্রন্টএন্ড লগইন পেজ (URL: jbdit.bd/login/) -> এটি এখন আর হোমে আসবে না
    path('login/', views.UserLoginView.as_view(), name='login'),

    # ৩. লগআউট পাথ (URL: jbdit.bd/logout/)
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    # Core Main Redirector Route
    path('dashboard/', views.dashboard_redirect_view, name='dashboard_redirect'),

    # 5 Isolated Secure Dashboard Paths
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/reception/', views.reception_dashboard, name='reception_dashboard'),
    path('dashboard/accounting/', views.accounting_dashboard, name='accounting_dashboard'),

    # User Management (CRUD)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserEditView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
