from django.urls import path
from .views import (
    StudentListView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView
)

urlpatterns = [
    path('list/', StudentListView.as_view(), name='student_list'),
    path('add/', StudentCreateView.as_view(), name='student_create'), # এই 'name' টি গুরুত্বপূর্ণ
    path('update/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
]
