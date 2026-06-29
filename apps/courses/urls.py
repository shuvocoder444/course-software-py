from django.urls import path
from .views import CourseView

urlpatterns = [
    # অন্যান্য URL...
    path('course-module/', CourseView.as_view(), name='course-module'),
]
