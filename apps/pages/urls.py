from django.urls import path

from .views import MiscPagesView

urlpatterns = [

    path(
        "student-certificate/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="certificate",
    ),
    path(
        "office-visitor/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="visitor",
    ),
    path(
        "contact-form-data/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="contact",
    ),

    path(
        "notification/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="notification",
    ),

    path(
        "ledger/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="ledger",
    ),


    path(
        "institute/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="ins",
    ),

    path(
        "info/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="info",
    ),
    path(
        "sms/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="sms",
    ),

    path(
        "slider/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="slider",
    ),
    path(
        "header/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="header",
    ),
    path(
        "about/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="about",
    ),
    path(
        "photo/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="photo",
    ),
    path(
        "video/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="video",
    ),
    path(
        "tutorial/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="tutorial",
    ),
    path(
        "students/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="students",
    ),


    path(
        "pages/misc/error/",
        MiscPagesView.as_view(template_name="pages_misc_error.html"),
        name="pages-misc-error",
    ),
    path(
        "pages/misc/under_maintenance/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="pages-misc-under-maintenance",
    ),
    path(
        "pages/misc/comingsoon/",
        MiscPagesView.as_view(template_name="pages_misc_comingsoon.html"),
        name="pages-misc-comingsoon",
    ),
    path(
        "pages/misc/not_authorized/",
        MiscPagesView.as_view(template_name="pages_misc_not_authorized.html"),
        name="pages-misc-not-authorized",
    ),
]
