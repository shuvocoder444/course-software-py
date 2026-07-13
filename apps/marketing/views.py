from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, View
from apps.account.views import VuxyVerticalLayoutMixin # আপনার মিক্সিন পাথ ঠিক রাখুন
from .models import Visitor, VisitorCategory
from .forms import VisitorForm, VisitorCategoryForm




# ==================== VISITOR CRUD ====================

from django.db.models import Q
# আপনার বাকি ইম্পোর্টগুলো (Mixin, Models) ঠিক রাখবেন...

class VisitorListView(LoginRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Visitor
    template_name = 'visitor-list.html'
    context_object_name = 'visitors'
    ordering = ['-id']
    paginate_by = 10  # প্রতি পেজে ১০ জন করে ভিজিটর দেখাবে

    def get_queryset(self):
        queryset = super().get_queryset()

        # URL থেকে সার্চ কিওয়ার্ড এবং ক্যাটাগরি আইডি নেওয়া
        search_query = self.request.GET.get('search', '')
        category_filter = self.request.GET.get('category', '')

        # নাম বা মোবাইল নাম্বার দিয়ে সার্চ ফিল্টার
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(mobile_number__icontains=search_query)
            )

        # ড্রপডাউন ক্যাটাগরি ফিল্টার
        if category_filter:
            queryset = queryset.filter(purpose_category_id=category_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ফিল্টার ড্রপডাউনে দেখানোর জন্য সব ক্যাটাগরি পাস করা হলো
        context['categories'] = VisitorCategory.objects.all()

        # ইউজার বর্তমানে কি ফিল্টার করেছে তা ইনপুট বক্সে ধরে রাখার জন্য
        context['selected_search'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

class VisitorCreateView(LoginRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Visitor
    form_class = VisitorForm
    template_name = 'visitor-create.html'
    success_url = reverse_lazy('visitor_list')

    def form_valid(self, form):
        messages.success(self.request, "Visitor added successfully!")
        return super().form_valid(form)

class VisitorEditView(LoginRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = Visitor
    form_class = VisitorForm
    template_name = 'visitor-create.html'
    success_url = reverse_lazy('visitor_list')

    def form_valid(self, form):
        messages.success(self.request, "Visitor updated successfully!")
        return super().form_valid(form)

class VisitorDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        visitor = get_object_or_404(Visitor, pk=pk)
        visitor.delete()
        messages.success(request, "Visitor deleted successfully!")
        return redirect('visitor_list')






from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, View
from apps.account.views import VuxyVerticalLayoutMixin # মিক্সিন পাথ চেক করে নিবেন
from .models import Visitor
from .forms import VisitorForm

# ==================== VISITOR CATEGORIES CRUD ====================

class VisitorCategoryListView(LoginRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = VisitorCategory
    template_name = 'visitor-catagories.html'
    context_object_name = 'categories'
    ordering = ['-id']

class VisitorCategoryCreateView(LoginRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = VisitorCategory
    form_class = VisitorCategoryForm
    template_name = 'visitor-catagories-form.html' # ক্রিয়েট ও এডিটের জন্য ছোট একটি ফর্ম টেমপ্লেট
    success_url = reverse_lazy('visitor_category_list')

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully!")
        return super().form_valid(form)

class VisitorCategoryEditView(LoginRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = VisitorCategory
    form_class = VisitorCategoryForm
    template_name = 'visitor-catagories-form.html'
    success_url = reverse_lazy('visitor_category_list')

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully!")
        return super().form_valid(form)

class VisitorCategoryDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(VisitorCategory, pk=pk)
        try:
            category.delete()
            messages.success(request, "Category deleted successfully!")
        except Exception:
            messages.error(request, "Cannot delete category! It is being used by some visitors.")
        return redirect('visitor_category_list')


# ==================== VISITOR CRUD ====================

class VisitorListView(LoginRequiredMixin, VuxyVerticalLayoutMixin, ListView):
    model = Visitor
    template_name = 'visitor-list.html'
    context_object_name = 'visitors'
    ordering = ['-id']

class VisitorCreateView(LoginRequiredMixin, VuxyVerticalLayoutMixin, CreateView):
    model = Visitor
    form_class = VisitorForm
    template_name = 'visitor-create.html'
    success_url = reverse_lazy('visitor_list')

    def form_valid(self, form):
        messages.success(self.request, "Visitor added successfully!")
        return super().form_valid(form)

class VisitorEditView(LoginRequiredMixin, VuxyVerticalLayoutMixin, UpdateView):
    model = Visitor
    form_class = VisitorForm
    template_name = 'visitor-create.html'
    success_url = reverse_lazy('visitor_list')

    def form_valid(self, form):
        messages.success(self.request, "Visitor updated successfully!")
        return super().form_valid(form)

class VisitorDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        visitor = get_object_or_404(Visitor, pk=pk)
        visitor.delete()
        messages.success(request, "Visitor deleted successfully!")
        return redirect('visitor_list')
