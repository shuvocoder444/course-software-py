from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

# আপনার অ্যাকাউন্টস অ্যাপ থেকে কাস্টম সিকিউরিটি ও লেআউট মিক্সিন ইম্পোর্ট
from apps.account.views import VuxyVerticalLayoutMixin, AdminRoleRequiredMixin

# বর্তমান অ্যাপের মডেল এবং ফর্ম ইম্পোর্ট
from .models import Course, Batch
from .forms import CourseForm, BatchForm

# ==============================================================================
# ১. COURSE MANAGEMENT CRUD VIEWS
# ==============================================================================

# ১. COURSE LIST VIEW
class CourseListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'courses/course_list.html'
    ordering = ['-id']


# ২. CREATE COURSE VIEW
class CourseCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        course = form.save()
        messages.success(self.request, f"Course '{course.name}' created successfully!")
        return super().form_valid(form)


# ৩. EDIT / UPDATE COURSE VIEW
class CourseEditView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, "Course information updated successfully!")
        return super().form_valid(form)


# ৪. DELETE COURSE VIEW
class CourseDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk):
        course_instance = get_object_or_404(Course, pk=pk)
        course_name = course_instance.name
        course_instance.delete()
        messages.success(request, f"Course '{course_name}' and its related batches deleted successfully!")
        return redirect('course_list')

    def get(self, request, pk):
        return self.post(request, pk)






    # ==============================================================================
# ২. BATCH MANAGEMENT CRUD VIEWS
# ==============================================================================

# ১. BATCH LIST VIEW
class BatchListView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Batch
    context_object_name = 'batches'
    template_name = 'courses/batch_list.html'
    ordering = ['-id']

    def get_queryset(self):
        # Database optimization এর জন্য select_related ব্যবহার করা হয়েছে
        return Batch.objects.select_related('course').all().order_by('-id')


# ২. CREATE BATCH VIEW
class BatchCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'courses/batch_form.html'
    success_url = reverse_lazy('batch_list')

    def form_valid(self, form):
        batch = form.save()
        messages.success(self.request, f"Batch '{batch.batch_number}' for {batch.course.name} created successfully!")
        return super().form_valid(form)


# ৩. EDIT / UPDATE BATCH VIEW
class BatchEditView(LoginRequiredMixin, AdminRoleRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = 'courses/batch_form.html'
    success_url = reverse_lazy('batch_list')

    def form_valid(self, form):
        messages.success(self.request, "Batch details updated successfully!")
        return super().form_valid(form)


# ৪. DELETE BATCH VIEW
class BatchDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, View):
    def post(self, request, pk):
        batch_instance = get_object_or_404(Batch, pk=pk)
        batch_name = batch_instance.batch_number
        batch_instance.delete()
        messages.success(request, f"Batch '{batch_name}' deleted successfully!")
        return redirect('batch_list')

    def get(self, request, pk):
        return self.post(request, pk)
