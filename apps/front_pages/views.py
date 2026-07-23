from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from .models import Slider, AboutContent, CardItem  # CardItem মডেল ইম্পোর্ট করা হলো
from apps.courses.models import Course, CourseReview
from .models import BlogPost
from apps.students.models import Student

class FrontPagesView(TemplateView):
    template_name = "index.html"  # আপনার ফ্রন্টএন্ডের মূল টেমপ্লেটের নাম

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # স্লাইডার কুয়েরি
        try:
            active_sliders = Slider.objects.filter(is_active=True)
        except Exception:
            active_sliders = Slider.objects.all()

        courses = Course.objects.all().order_by('-created_at')
        latest_posts = BlogPost.objects.filter(is_published=True).order_by('-published_at')[:5]
        marquee_students = Student.objects.filter(status='approved').order_by('-id')[:10]
        testimonials = CourseReview.objects.all().select_related('user', 'course').order_by('-created_at')[:8]

        # ডাইনামিক About সেকশন কুয়েরি
        try:
            about_data = AboutContent.objects.first()
        except Exception:
            about_data = None




        # ================= Front Course (CardItem) Query =================
        front_courses = CardItem.objects.all()
        first_card = front_courses.first()

        section_title = first_card.section_title if (first_card and first_card.section_title) else "চলতি অফলাইন প্রিমিয়াম ব্যাচসমূহ"
        section_description = first_card.section_description if (first_card and first_card.section_description) else "ল্যাব ও মাল্টিমিডিয়া প্রজেক্টর সাপোর্টেড ক্লাসরুম শিডিউল"
        # =================================================================

        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,
                "sliders": active_sliders,
                "courses": courses,
                "latest_posts": latest_posts,
                "marquee_students": marquee_students,
                "testimonials": testimonials,
                "about_data": about_data,

                # Front Course Data
                "front_courses": front_courses,
                "section_title": section_title,
                "section_description": section_description,
            }
        )

        TemplateHelper.map_context(context)
        return context



from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

class CourseDetailView(TemplateView):
    template_name = "single.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # ইউআরএল থেকে স্ল্যাগ (slug) নিয়ে কোর্স অবজেক্টটি খোঁজা হচ্ছে
        course_slug = self.kwargs.get('slug')
        course = get_object_or_404(Course, slug=course_slug)

        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,
                "course": course,
                "title": course.name,
            }
        )

        TemplateHelper.map_context(context)
        return context



from django.views.generic import ListView
from django.db.models import Q

from apps.front_pages.models import Category
from django.template.loader import render_to_string
from django.http import HttpResponse


class BlogFeedView(ListView):
    model = BlogPost
    template_name = "blog.html"
    context_object_name = "blog_posts"
    paginate_by = 20

    def get_queryset(self):
        qs = BlogPost.objects.filter(is_published=True).order_by('-published_at')

        search = self.request.GET.get('q')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(content__icontains=search))

        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__slug=category)

        return qs

    def render_to_response(self, context, **response_kwargs):
        # AJAX রিকোয়েস্ট হলে শুধু গ্রিড + পেজিনেশন পার্ট পাঠাবে
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('blog_grid_partial.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, context)

        context["categories"] = Category.objects.all()

        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,
            }
        )

        TemplateHelper.map_context(context)

        return context



from django.views.generic import DetailView
class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        # সুপার ক্লাস থেকে ডিফল্ট কনটেক্সট (যেখানে 'post' অবজেক্ট থাকে) নিয়ে আসা
        context = super().get_context_data(**kwargs)

        # FrontPagesView এর মতো গ্লোবাল লেআউট ইনিশিয়ালাইজ করা
        context = TemplateLayout.init(self, context)

        # পোস্টের ভিউ কাউন্ট ১ বাড়িয়ে ডাটাবেজে সেভ করার লজিক
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])

        # সাইডবারের জন্য রিসেন্ট পোস্টের কুয়েরি (বর্তমান পোস্টটি বাদ দিয়ে)
        context['recent_posts'] = BlogPost.objects.filter(
            is_published=True
        ).exclude(
            id=self.object.id
        ).order_by('-published_at')[:5]

        # লেআউট পাথ এবং ফ্রন্টএন্ড কনটেক্সট আপডেট
        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,  # বর্তমান অ্যাক্টিভ ইউআরএল ট্র্যাক করা
            }
        )

        # কনটেক্সট ম্যাপিং
        TemplateHelper.map_context(context)

        return context


# =================================Slider Start ============================

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
# আপনার প্রজেক্টের সঠিক মিক্সিন পাথ অনুযায়ী এগুলো ইম্পোর্ট করুন
from apps.courses.views import LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin
from .forms import SliderForm
from django.views.generic import ListView, UpdateView, DeleteView
# আপনার মিক্সিন এবং মডেল ইম্পোর্ট

# ১. SLIDER LIST VIEW
class SliderListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Slider
    template_name = 'backend/slider_list.html'
    context_object_name = 'sliders'

# ২. SLIDER CREATE VIEW
class SliderCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Slider
    form_class = SliderForm
    template_name = 'backend/slider.html'
    success_url = reverse_lazy('slider_list') # এখন এটি সরাসরি লিস্ট পেজে নিয়ে যাবে

    def form_valid(self, form):
        slider = form.save()
        messages.success(self.request, "Slider created successfully!")
        return super().form_valid(form)

# ৩. SLIDER UPDATE VIEW
class SliderUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = Slider
    form_class = SliderForm
    template_name = 'backend/slider.html' # ক্রিয়েট এবং আপডেট একই ফর্মে হ্যান্ডেল হবে
    success_url = reverse_lazy('slider_list')

    def form_valid(self, form):
        slider = form.save()
        messages.success(self.request, "Slider updated successfully!")
        return super().form_valid(form)

# ৪. SLIDER DELETE VIEW
class SliderDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = Slider
    success_url = reverse_lazy('slider_list')

    # ডিলিট করার পর সাকসেস মেসেজ দেখানোর জন্য
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Slider deleted successfully!")
        return super().delete(request, *args, **kwargs)




# =================================ABOUT US Start ============================

from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import AboutFeature
from .forms import AboutContentForm, AboutFeatureFormSet
from apps.courses.views import LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin


class AboutContentManageView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = AboutContent
    form_class = AboutContentForm
    template_name = 'backend/about_manage.html'
    success_url = reverse_lazy('about_manage')

    def get_object(self, queryset=None):
        obj, created = AboutContent.objects.get_or_create(id=1)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['left_features_list'] = AboutFeature.objects.filter(about_content=self.object).order_by('order', 'id')

        if self.request.method == 'POST':
            context['feature_formset'] = AboutFeatureFormSet(self.request.POST, instance=self.object, prefix='features')
        else:
            context['feature_formset'] = AboutFeatureFormSet(instance=self.object, prefix='features')

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        feature_formset = context['feature_formset']

        if form.is_valid() and feature_formset.is_valid():
            self.object = form.save()
            feature_formset.instance = self.object
            feature_formset.save()

            messages.success(self.request, "About section updated successfully!")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong! Please check the form errors.")
        return super().form_invalid(form)

# ==================================FRONT Course ================================
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.courses.views import LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin
from .forms import CardItemForm, SectionHeaderForm


# ================================= FRONT COURSE LIST ============================
class FrontCourseListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = CardItem
    template_name = 'backend/frontcourse_list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # প্রথম অবজেক্ট থেকে সেকশন টাইটেল ও ডেসক্রিপশন কন্টেক্সটে পাঠানো হচ্ছে
        first_item = CardItem.objects.first()
        context['section_info'] = first_item
        context['header_form'] = SectionHeaderForm(instance=first_item) if first_item else SectionHeaderForm()
        return context


# ================================= UPDATE SECTION HEADER ============================
def update_section_header(request):
    if request.method == 'POST':
        first_item = CardItem.objects.first()
        if first_item:
            # বিদ্যমান সব কার্ডের সেকশন টাইটেল ও ডেসক্রিপশন একসাথে আপডেট হবে
            form = SectionHeaderForm(request.POST, instance=first_item)
            if form.is_valid():
                title = form.cleaned_data['section_title']
                desc = form.cleaned_data['section_description']
                CardItem.objects.all().update(section_title=title, section_description=desc)
                messages.success(request, "Section header updated for all courses!")
        else:
            messages.error(request, "Please create at least one course first.")
    return redirect('frontcourse_list')



# ================================= FRONT COURSE CREATE ============================
class FrontCourseCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = CardItem
    form_class = CardItemForm
    template_name = 'backend/frontcourse_manage.html'
    success_url = reverse_lazy('frontcourse_list')

    def form_valid(self, form):
        # ডাটাবেজে ইতোমধ্যে কোনো কার্ড থাকলে সেখান থেকে সেকশন হেডার কপি করে বসাবে
        first_item = CardItem.objects.first()
        if first_item and first_item.section_title:
            form.instance.section_title = first_item.section_title
            form.instance.section_description = first_item.section_description

        messages.success(self.request, "Course created successfully!")
        return super().form_valid(form)

# ================================= FRONT COURSE UPDATE ============================
class FrontCourseUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = CardItem
    form_class = CardItemForm  # <--- CardItem-এর বদলে CardItemForm ব্যবহার করা হয়েছে
    template_name = 'backend/frontcourse_manage.html'
    success_url = reverse_lazy('frontcourse_list')

    def form_valid(self, form):
        messages.success(self.request, "Course updated successfully!")
        return super().form_valid(form)


# ================================= FRONT COURSE DELETE ============================
class FrontCourseDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, DeleteView):
    model = CardItem
    success_url = reverse_lazy('frontcourse_list')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Course deleted successfully!")
        return super().post(request, *args, **kwargs)


# ================================= FRONT COURSE Details ============================






from django.views.generic import DetailView
from .models import CardItem


class FrontCardDetailView(DetailView):
    model = CardItem
    template_name = 'frontcourse_detail.html'
    context_object_name = 'card'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        slug_or_pk = self.kwargs.get('slug')

        if str(slug_or_pk).isdigit():
            return get_object_or_404(CardItem, pk=int(slug_or_pk))

        return get_object_or_404(CardItem, slug=slug_or_pk)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # 💥 সাইডবারের জন্য বর্তমান কোর্সটি ছাড়া অন্য সব কোর্স কুয়েরি করা হচ্ছে
        context['other_courses'] = CardItem.objects.exclude(id=self.object.id)

        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,
            }
        )

        TemplateHelper.map_context(context)
        return context



# =================================BLOG Start============================

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.http import HttpResponseRedirect

# আপনার প্রজেক্টের সঠিক মিক্সিন ও মডেল পাথ
from apps.courses.views import LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin
from .models import BlogPost
from .forms import BlogPostForm

# ================= ১. BLOG LIST VIEW  =================
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.front_pages.models import BlogPost  # আপনার সঠিক মডেল পাথটি ব্যবহার করুন

class BlogPostListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = BlogPost
    template_name = 'backend/blog_list_manage.html'
    context_object_name = 'posts'
    ordering = ['-published_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # ১. ক্যাটাগরি ফিল্টার ড্রপডাউন
        category_id = self.request.GET.get('category', '')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # ২. স্ট্যাটাস ফিল্টার ড্রপডাউন
        status_filter = self.request.GET.get('status', '')
        if status_filter == 'published':
            queryset = queryset.filter(is_published=True)
        elif status_filter == 'draft':
            queryset = queryset.filter(is_published=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ড্রপডাউনে সিলেক্টেড ভ্যালু ধরে রাখা এবং সব ক্যাটাগরি লিস্ট দেখানোর জন্য
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context

# ================= ২. BLOG CREATE VIEW =================
class BlogPostCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'backend/blog_manage.html'
    success_url = reverse_lazy('blog_list_manage')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user

        title = form.cleaned_data.get('title', '')
        generated_slug = slugify(title, allow_unicode=True)

        original_slug = generated_slug
        queryset = BlogPost.objects.filter(slug=generated_slug)
        count = 1
        while queryset.exists():
            generated_slug = f"{original_slug}-{count}"
            count += 1
            queryset = BlogPost.objects.filter(slug=generated_slug)

        self.object.slug = generated_slug
        self.object.save()
        form.save_m2m()

        messages.success(self.request, "Blog post created successfully!")
        return HttpResponseRedirect(self.get_success_url())


# ================= ৩. BLOG UPDATE VIEW =================
class BlogPostUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'backend/blog_manage.html'
    success_url = reverse_lazy('blog_list_manage')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        title = form.cleaned_data.get('title', '')
        generated_slug = slugify(title, allow_unicode=True)

        original_slug = generated_slug
        queryset = BlogPost.objects.filter(slug=generated_slug).exclude(pk=self.object.pk)
        count = 1
        while queryset.exists():
            generated_slug = f"{original_slug}-{count}"
            count += 1
            queryset = BlogPost.objects.filter(slug=generated_slug).exclude(pk=self.object.pk)

        self.object.slug = generated_slug
        self.object.save()
        form.save_m2m()

        messages.success(self.request, "Blog post updated successfully!")
        return HttpResponseRedirect(self.get_success_url())


# ================= ৪. BLOG DELETE VIEW =================


class BlogPostDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog_list_manage')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Blog post deleted successfully!")
        return super().delete(request, *args, **kwargs)





from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import CategoryForm

# ১. সিঙ্গেল ম্যানেজমেন্ট পেজ (লিস্ট ভিউ)
class CategoryManageView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Category
    template_name = 'backend/category_manage.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryForm()
        return context


# ২. AJAX ক্রিয়েট ভিউ
@login_required
@require_POST
def quick_category_create(request):
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'success': False, 'error': 'Category name cannot be empty.'}, status=400)

    # allow_unicode=True দেওয়ার ফলে বাংলা অক্ষরগুলো স্ল্যাগ হিসেবে কাজ করবে
    generated_slug = slugify(name, allow_unicode=True)

    try:
        # স্লাগ ইতিমধ্যে আছে কিনা চেক করা
        if Category.objects.filter(slug=generated_slug).exists():
            return JsonResponse({'success': False, 'error': 'A category with this name or slug already exists.'}, status=400)

        # সরাসরি ক্রিয়েট করা
        category = Category.objects.create(
            name=name,
            slug=generated_slug
        )

        return JsonResponse({
            'success': True,
            'id': category.id,
            'name': category.name,
            'slug': category.slug,  # ফ্রন্টএন্ডে দেখানোর জন্য স্লাগ পাঠানো হলো
            'created': True
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ৩. AJAX আপডেট ভিউ
@login_required
@require_POST
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    name = request.POST.get('name', '').strip()

    # ইনপুট ফিল্ডে ইউজার যদি নিজে স্লাগ লিখে দেয়, তবে সেটা নেওয়া হবে। না দিলে নাম থেকে জেনারেট হবে।
    custom_slug = request.POST.get('slug', '').strip()

    if not name:
        return JsonResponse({'success': False, 'error': 'Category name cannot be empty.'}, status=400)

    if custom_slug:
        generated_slug = slugify(custom_slug, allow_unicode=True)
    else:
        generated_slug = slugify(name, allow_unicode=True)

    try:
        # নিজের আইডি বাদে অন্য কারও সাথে স্লাগ মিলছে কিনা চেক
        if Category.objects.filter(slug=generated_slug).exclude(pk=pk).exists():
            return JsonResponse({'success': False, 'error': 'Another category with this slug already exists.'}, status=400)

        category.name = name
        category.slug = generated_slug
        category.save()

        return JsonResponse({
            'success': True,
            'id': category.id,
            'name': category.name,
            'slug': category.slug  # আপডেট হওয়া স্লাগ পাঠানো হলো
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ৪. AJAX ডিলিট ভিউ
@login_required
@require_POST
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    try:
        category.delete()
        return JsonResponse({'success': True, 'message': 'Category deleted successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
