from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages  # ইউজারকে মেসেজ দেখানোর জন্য
from .models import Student
from .forms import StudentForm

# কোর লেআউট ইমপোর্ট
from web_project import TemplateLayout, TemplateHelper

# ১. স্টুডেন্ট লিস্ট ভিউ
class StudentListView(ListView):
    model = Student
    template_name = "student.html"
    context_object_name = "students"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout": "vertical",
            "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        })
        return context

# ২. স্টুডেন্ট ক্রিয়েট ভিউ
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, "Student added successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout": "vertical",
            "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            "title": "Add New Student"
        })
        return context

# ৩. স্টুডেন্ট আপডেট ভিউ
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, "Student updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout": "vertical",
            "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            "title": "Update Student"
        })
        return context

# ৪. স্টুডেন্ট ডিলিট ভিউ
class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('student_list')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Student deleted successfully!")
        return super().post(request, *args, **kwargs)
