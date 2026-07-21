# =================================Slider Start ============================

from django import forms
from .models import Slider

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = [
            'title_white', 'title_colored', 'description',
            'btn1_text', 'btn1_url', 'btn2_text', 'btn2_url',
            'right_image', 'order', 'is_active'
        ]
        # বুটস্ট্র্যাপ ডিজাইনের সাথে মেলানোর জন্য উইজেট ক্লাস যুক্ত করতে পারেন
        widgets = {
            'title_white': forms.TextInput(attrs={'class': 'form-control'}),
            'title_colored': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'btn1_text': forms.TextInput(attrs={'class': 'form-control'}),
            'btn1_url': forms.TextInput(attrs={'class': 'form-control'}),
            'btn2_text': forms.TextInput(attrs={'class': 'form-control'}),
            'btn2_url': forms.TextInput(attrs={'class': 'form-control'}),
            'right_image': forms.FileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# =================================ABOUT US Start ============================

# apps/front_pages/forms.py
from django import forms
from .models import AboutContent

class AboutContentForm(forms.ModelForm):
    class Meta:
        model = AboutContent
        fields = ['title_white', 'description', 'btn_text', 'btn_url', 'right_image']
        widgets = {
            'title_white': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: Building Careers,'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Main description paragraph text'}),
            'btn_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: Learn More'}),
            'btn_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: /about-us/'}),
            'right_image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


# =================================Blog Start ============================

from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            'title', 'content', 'category', 'featured_image',
            'image_alt_text', 'meta_title',
            'meta_description', 'focus_keyword', 'is_published', 'read_time_minutes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your content here...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_alt_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image alt text for SEO'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select select2'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 60}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 160}),
            'focus_keyword': forms.TextInput(attrs={'class': 'form-control'}),
            'read_time_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }
