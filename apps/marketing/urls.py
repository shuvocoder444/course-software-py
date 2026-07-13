from django.urls import path
from .views import (
    VisitorListView, VisitorCreateView, VisitorEditView, VisitorDeleteView,
    VisitorCategoryListView, VisitorCategoryCreateView, VisitorCategoryEditView, VisitorCategoryDeleteView
)

urlpatterns = [
    # Visitor URLs
    path('list/', VisitorListView.as_view(), name='visitor_list'),
    path('add/', VisitorCreateView.as_view(), name='visitor_create'),
    path('edit/<int:pk>/', VisitorEditView.as_view(), name='visitor_edit'),
    path('delete/<int:pk>/', VisitorDeleteView.as_view(), name='visitor_delete'),

    # Category URLs (ক্রিয়েট, আপডেট এবং ডিলিট)
    path('categories/list/', VisitorCategoryListView.as_view(), name='visitor_category_list'),
    path('categories/add/', VisitorCategoryCreateView.as_view(), name='visitor_category_create'),
    path('categories/edit/<int:pk>/', VisitorCategoryEditView.as_view(), name='visitor_category_edit'),
    path('categories/delete/<int:pk>/', VisitorCategoryDeleteView.as_view(), name='visitor_category_delete'),
]
