# urls.py (আপনার অ্যাপ ফোল্ডারের ভেতর)
from django.urls import path

from .views import InstituteSettingDeleteView, InstituteSettingView

urlpatterns = [
    # প্রধান ভিউ এবং আপডেট ইউআরএল
    path('institute/', InstituteSettingView.as_view(), name='institute'),

    # ডিলিট করার ইউআরএল
    path('institute/delete/<int:pk>/', InstituteSettingDeleteView.as_view(), name='delete_institute_setting'),
]
