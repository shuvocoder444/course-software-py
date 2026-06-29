from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

@admin.register(Account)
class AccountAdmin(UserAdmin):
    # ইউজার লিস্ট পেজে যা যা দেখাবে
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')

    # ফিল্টার করার সুবিধা (যেমন: রোল অনুযায়ী ইউজার দেখা)
    list_filter = ('role', 'is_staff', 'is_superuser')

    # ইউজার এডিট পেজে 'role' ফিল্ডটি যোগ করা
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

    # নতুন ইউজার তৈরির সময় 'role' ফিল্ডটি দেখানোর জন্য
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

    # সার্চ করার অপশন
    search_fields = ('username', 'email', 'role')
