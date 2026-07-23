from django.urls import path

# আলাদা আলাদা ভিউ ইমপোর্ট না করে সরাসরি পুরো views মডিউলটি ইমপোর্ট করা হলো
from . import views

urlpatterns = [
    # ফ্রন্টপেজ ভিউসমূহ
    path("", views.FrontPagesView.as_view(template_name="landing_page.html"), name="landing-page"),
    path("about/", views.FrontPagesView.as_view(template_name="about.html"), name="about"),
    path("contact/", views.FrontPagesView.as_view(template_name="contact.html"), name="contact"),
    path("courses/", views.FrontPagesView.as_view(template_name="courses.html"), name="courses"),

    # ফন্ট কোর্সসমূহ
    path("office-application/", views.FrontPagesView.as_view(template_name="officeapplication.html"), name="officeapplication"),
    path("graphics-design/", views.FrontPagesView.as_view(template_name="graphicsdesign.html"), name="graphicsdesign"),
    path("digital-marketing/", views.FrontPagesView.as_view(template_name="digitalmarketing.html"), name="digitalmarketing"),
    path("video-editing/", views.FrontPagesView.as_view(template_name="videoediting.html"), name="videoediting"),
    path("wordpress-development/", views.FrontPagesView.as_view(template_name="wordpressdevelopment.html"), name="wordpressdevelopment"),
    path("instructors/", views.FrontPagesView.as_view(template_name="instructors.html"), name="instructors"),
    path("photo-gallery/", views.FrontPagesView.as_view(template_name="photo_gallery.html"), name="photo-gallery"),
    path("students/", views.FrontPagesView.as_view(template_name="students.html"), name="students"),
    path("tutorials/", views.FrontPagesView.as_view(template_name="tutorials.html"), name="tutorials"),
    path("video-gallery/", views.FrontPagesView.as_view(template_name="video_gallery.html"), name="video-gallery"),

    # কোর্স ডিটেইলস
    path('backend/about/manage/', views.AboutContentManageView.as_view(), name='about_manage'),
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    # ব্যাকএন্ড ক্রুড (CRUD) ভিউস
    path('blog/', views.BlogFeedView.as_view(), name='blog_feed'),
    path('backend/blog/list/', views.BlogPostListView.as_view(), name='blog_list_manage'),
    path('blog/<str:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('backend/blog/create/', views.BlogPostCreateView.as_view(), name='blog_create'),
    path('backend/blog/edit/<int:pk>/', views.BlogPostUpdateView.as_view(), name='blog_manage'),
    path('backend/blog/delete/<int:pk>/', views.BlogPostDeleteView.as_view(), name='blog_delete'),
    path('backend/blog/category/', views.CategoryManageView.as_view(), name='category_manage'),
    path('backend/blog/category/quick-create/', views.quick_category_create, name='quick_category_create'),
    path('backend/blog/category/update/<int:pk>/', views.category_update, name='category_update'),
    path('backend/blog/category/delete/<int:pk>/', views.category_delete, name='category_delete'),


    # ফন্ট-কোর্স ম্যানেজমেন্ট (ব্যাকএন্ড)
    path('front-courses/', views.FrontCourseListView.as_view(), name='frontcourse_list'),
    path('front-courses/update-header/', views.update_section_header, name='update_section_header'),
    path('front-courses/create/', views.FrontCourseCreateView.as_view(), name='frontcourse_create'),
    path('front-courses/<int:pk>/edit/', views.FrontCourseUpdateView.as_view(), name='frontcourse_update'),
    path('front-courses/<int:pk>/delete/', views.FrontCourseDeleteView.as_view(), name='frontcourse_delete'),
    path('front-course/<slug:slug>/', views.FrontCardDetailView.as_view(), name='card_detail'),






    # স্লাইডার ম্যানেজমেন্ট (ব্যাকএন্ড)
    path('backend/slider/list/', views.SliderListView.as_view(), name='slider_list'),
    path('backend/slider/create/', views.SliderCreateView.as_view(), name='slider_create'),
    path('backend/slider/edit/<int:pk>/', views.SliderUpdateView.as_view(), name='slider_edit'),
    path('backend/slider/delete/<int:pk>/', views.SliderDeleteView.as_view(), name='slider_delete'),



]
