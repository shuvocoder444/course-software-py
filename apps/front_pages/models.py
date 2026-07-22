
# Create your models here.
# =================================Slider Start ============================

from django.db import models

class Slider(models.Model):
    title_white = models.CharField(max_length=255, blank=True, null=True, help_text="Example: Build Real Projects")
    title_colored = models.CharField(max_length=255, blank=True, null=True, help_text="Example: For Your Portfolio")
    description = models.TextField(blank=True, null=True, help_text="Slider main paragraph text")

    # Buttons
    btn1_text = models.CharField(max_length=50, blank=True, null=True, help_text="Example: See Curriculum")
    btn1_url = models.CharField(max_length=500, blank=True, null=True)
    btn2_text = models.CharField(max_length=50, blank=True, null=True, help_text="Example: Student Stories")
    btn2_url = models.CharField(max_length=500, blank=True, null=True)

    # Right Side Content (Image or Vector)
    right_image = models.ImageField(upload_to='sliders/', blank=True, null=True, help_text="Right side graphical showcase image")

    # Ordering & Active status
    order = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"

    def __str__(self):
        return f"{self.title_white} {self.title_colored}" if self.title_white or self.title_colored else f"Slider #{self.id}"

# =================================Slider End ============================



# =================================ABOUT US Start ============================


from django.db import models

class AboutContent(models.Model):
    # RIGHT SIDE (Fixed Fields)
    right_title = models.CharField(max_length=255, blank=True, null=True, help_text="Right Side Main Title")
    right_title_color = models.CharField(max_length=50, blank=True, null=True, default="#FFFFFF")
    right_description = models.TextField(blank=True, null=True)
    right_btn_text = models.CharField(max_length=50, blank=True, null=True)
    right_btn_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "About Content"
        verbose_name_plural = "About Content"

    def __str__(self):
        return self.right_title or "About Content Section"


class AboutFeature(models.Model):
    # LEFT SIDE (Multiple Cards with CRUD)
    about_content = models.ForeignKey(AboutContent, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True, help_text="Card Title")
    title_color = models.CharField(max_length=50, blank=True, null=True, default="#FFFFFF")
    description = models.TextField(blank=True, null=True, help_text="Card Description")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f"Feature #{self.id}"


# =================================ABOUT US  End============================




# =================================OUR COURSES Start============================
from django.db import models
from django.utils.text import slugify

class CardItem(models.Model):
    section_title = models.CharField(blank=True, null=True, max_length=200, help_text="সেকশনের মেইন টাইটেল")
    section_description = models.TextField(blank=True, null=True, help_text="সেকশনের বিবরণ")

    image = models.ImageField(blank=True, null=True, upload_to='card_images/', help_text="কোর্স ছবি")
    title = models.CharField(blank=True, null=True, max_length=200, help_text="কোর্স টাইটেল")

    # URL-এর জন্য ইউনিক স্ল্যাগ ফিল্ড
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=250, help_text="URL Slug (খালি রাখলে অটো জেনারেট হবে)")

    title_color = models.CharField(max_length=20, default="#000000", help_text="HEX বা Color Name")
    description = models.TextField(blank=True, null=True, help_text="কোর্স বিবরণ")
    button_link = models.URLField(blank=True, null=True, help_text="খালি রাখলে সিঙ্গেল পেজে নিয়ে যাবে")

    def save(self, *args, **kwargs):
        # স্ল্যাগ না থাকলে অটো জেনারেট করবে
        if not self.slug:
            base_title = self.title if self.title else "course"
            base_slug = slugify(base_title, allow_unicode=True)

            # টাইটেল যদি সম্পূর্ণরূপে স্পেশাল ক্যারেক্টার হয় এবং slugify খালি আউটপুট দেয়
            if not base_slug:
                base_slug = "course"

            slug = base_slug
            counter = 1

            # ডাটাবেজে একই স্ল্যাগ অন্য কোনো অবজেক্টে আছে কিনা চেক করে ইউনিক স্ল্যাগ তৈরি করবে
            while CardItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Card Item"
# =================================OUR COURSES  End============================



# =================================STUDENT Review Start============================


# =================================STUDENT Review  End============================



# =================================BLOG Start============================
from django.db import models
from django.conf import settings
from django.urls import reverse  # ১. এটি অবশ্যই ইম্পোর্ট করবেন

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    published_at = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    featured_image = models.ImageField(upload_to='blog/images/')
    image_alt_text = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    # SEO Fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    focus_keyword = models.CharField(max_length=100, blank=True)

    # Metrics & Status
    is_published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    read_time_minutes = models.PositiveIntegerField(default=5)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # ২. এই মেথডটি ক্লাসের ভেতরে যুক্ত করুন
    def get_absolute_url(self):
        # 'blog_detail' এর জায়গায় আপনার urls.py এ ডিফাইন করা name টি বসাবেন
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
# =================================BLOG  End============================



# =================================Students Joining  Start============================


# =================================Students Joining End============================
