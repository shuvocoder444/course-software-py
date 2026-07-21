
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

class AboutContent(models.Model):
    title_white = models.CharField(max_length=255, blank=True, null=True, help_text="Example: Building Careers,")
    description = models.TextField(blank=True, null=True, help_text="Main description paragraph text")

    # Button
    btn_text = models.CharField(max_length=50, blank=True, null=True, help_text="Example: Learn More")
    btn_url = models.CharField(max_length=500, blank=True, null=True)

    # Image
    right_image = models.ImageField(upload_to='about/', blank=True, null=True, help_text="Background or Section Image")

    class Meta:
        verbose_name = "About Content"
        verbose_name_plural = "About Content"

    def __str__(self):
        return f"{self.title_white} {self.title_colored}" if self.title_white or self.title_colored else "About Content"

# =================================ABOUT US  End============================




# =================================OUR COURSES Start============================


# =================================OUR COURSES  End============================



# =================================STUDENT Review Start============================


# =================================STUDENT Review  End============================



# =================================BLOG Start============================
from django.db import models
from django.utils.text import slugify
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
