from django.conf import settings  # 👑 মিডিয়া সেটিংস ইমপোর্ট করা হলো
from django.conf.urls.static import static  # 👑 স্ট্যাটিক রুট ইমপোর্ট করা হলো
from django.contrib import admin
from django.urls import include, path

from web_project.views import SystemView

urlpatterns = [
    path("admin/", admin.site.urls),

    # starter urls
    path("sample/", include("apps.sample.urls")),

    # pages urls
    path("pages/", include("apps.pages.urls")),

    # users & accounts urls
    path('account/', include('apps.account.urls')),

    # frontend/home pages urls
    path('', include('apps.front_pages.urls')),

    # ড্যাশবোর্ড ইউআরএল
    path("dashboard/courses/", include("apps.courses.urls")),
    path('dashboard/students/', include('apps.students.urls')),
    path('dashboard/finance/', include('apps.finance.urls')),
    path('dashboard/marketing/', include('apps.marketing.urls')),
    path('dashboard/settings/', include('apps.setting.urls')),
]

# 👑 লোকাল ডেভেলপমেন্টে (DEBUG=True) আপলোড করা ছবি দেখার জন্য মিডিয়া ইউআরএল যুক্ত করা হলো
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom Error Handlers
handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler403 = SystemView.as_view(template_name="pages_misc_not_authorized.html", status=403)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
