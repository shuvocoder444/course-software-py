from django.urls import path

from . import views

urlpatterns = [
    # ক্রিয়েট এবং আপডেট দুটিই এই একটা সিঙ্গেল ইউআরএল দিয়েই হবে
    path('settings/', views.institute_settings_view, name='institute_settings'),
    path('sms-history/delete/', views.SMSLogDeleteView.as_view(), name='delete_sms_logs'),
    path('sms-history/', views.SMSHistoryListView.as_view(), name='sms_history'),
]
