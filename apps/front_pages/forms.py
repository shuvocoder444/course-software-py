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





from django import forms
from django.forms import inlineformset_factory
from .models import AboutContent, AboutFeature

class AboutContentForm(forms.ModelForm):
    class Meta:
        model = AboutContent
        fields = ['right_title', 'right_title_color', 'right_description', 'right_btn_text', 'right_btn_url']
        widgets = {
            'right_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter section title'}),
            'right_title_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color', 'title': 'Choose title color'}),
            'right_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter description'}),
            'right_btn_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Button text'}),
            'right_btn_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Button link/URL'}),
        }


class AboutFeatureForm(forms.ModelForm):
    class Meta:
        model = AboutFeature
        fields = ['title', 'title_color', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card title'}),
            'title_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color', 'title': 'Choose card title color'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Card description'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# 'features' prefix নিশ্চিত করার জন্য related_name অনুযায়ী inlineformset তৈরি
AboutFeatureFormSet = inlineformset_factory(
    AboutContent,
    AboutFeature,
    form=AboutFeatureForm,
    extra=0,
    can_delete=True
)



# =================================CardItemForm   US Start ============================
from django import forms
from .models import CardItem

# সেকশন হেডার আপডেট করার জন্য ফর্ম
class SectionHeaderForm(forms.ModelForm):
    class Meta:
        model = CardItem
        fields = ['section_title', 'section_description']
        labels = {
            'section_title': 'Section Title',
            'section_description': 'Section Description',
        }
        widgets = {
            'section_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter section title'}),
            'section_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter section description'}),
        }

# শুধু কার্ড/বক্স ম্যানেজ করার জন্য ফর্ম (আপডেট করা হয়েছে)
class CardItemForm(forms.ModelForm):
    class Meta:
        model = CardItem
        fields = ['image', 'title', 'slug', 'title_color', 'description', 'button_link']
        labels = {
            'image': 'Card Image',
            'title': 'Card Title',
            'slug': 'Custom Slug',
            'title_color': 'Title Color',
            'description': 'Card Description',
            'button_link': 'Custom Button Link',
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank for auto-generated slug'}),
            'title_color': forms.TextInput(attrs={'class': 'form-control form-control-color', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter course description'}),
            'button_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
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
