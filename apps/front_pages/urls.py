from django.urls import path

from .views import FrontPagesView

urlpatterns = [
    path(
        "",
        FrontPagesView.as_view(template_name="landing_page.html"),
        name="landing-page",
    ),
    path(
        "front/pricing/",
        FrontPagesView.as_view(template_name="pricing_page.html"),
        name="pricing-page",
    ),
    path(
        "front/payment/",
        FrontPagesView.as_view(template_name="payment_page.html"),
        name="payment-page",
    ),
    path(
        "front/checkout/",
        FrontPagesView.as_view(template_name="checkout_page.html"),
        name="checkout-page",
    ),
    path(
        "front/help_center/",
        FrontPagesView.as_view(template_name="help_center_landing.html"),
        name="help-center-landing",
    ),
    path(
        "front/help_center/article/",
        FrontPagesView.as_view(template_name="help_center_article.html"),
        name="help-center-article",
    ),


    path("about/", FrontPagesView.as_view(template_name="about.html"), name="about"),
    path("contact/", FrontPagesView.as_view(template_name="contact.html"), name="contact"),
    path("courses/", FrontPagesView.as_view(template_name="courses.html"), name="courses"),
    path("photo-gallery/", FrontPagesView.as_view(template_name="photo_gallery.html"), name="photo-gallery"),
    path("students/", FrontPagesView.as_view(template_name="students.html"), name="students"),
    path("tutorials/", FrontPagesView.as_view(template_name="tutorials.html"), name="tutorials"),
    path("video-gallery/", FrontPagesView.as_view(template_name="video_gallery.html"), name="video-gallery"),
]
