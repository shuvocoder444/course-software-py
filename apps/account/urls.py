from django.urls import path
from . import views  # সব ভিউ ইমপোর্ট হলো
# apps/account/urls.py ফাইলে শুধু urlpatterns অংশটি এভাবে পরিবর্তন করুন:

urlpatterns = [
    # Auth Routes
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.StudentAjaxRegisterView.as_view(), name='student_register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    # Core Main Redirector Route
    # 🟢 এটিকে পুরোপুরি খালি রাখুন, কারণ রুট ফাইলের 'dashboard/account/' ই একে হ্যান্ডেল করবে
    path('', views.dashboard_redirect_view, name='dashboard_redirect'),

    # 🟢 ৫টি ড্যাশবোর্ডের পাথ থেকে অতিরিক্ত 'dashboard/' কেটে শুধু নামগুলো রাখুন:
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('reception/', views.reception_dashboard, name='reception_dashboard'),
    path('accounting/', views.accounting_dashboard, name='accounting_dashboard'),

    # User Management (CRUD)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserEditView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
