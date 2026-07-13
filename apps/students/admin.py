from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # অ্যাডমিন লিস্ট ভিউতে যে ফিল্ডগুলো কলাম আকারে দেখাবে
    list_display = (
        'student_id',
        'name',
        'course',
        'batch',
        'phone',
        'session',
        'status',
        'submitted_at'
    )

    # এই লাইনটি যুক্ত করুন: এর ফলে student_id এবং name দুটোর ওপর ক্লিক করলেই এডিট পেজে যাবে
    # (যদি student_id কখনো খালিও থাকে, নামের ওপর ক্লিক করে ঢুকতে পারবেন)
    list_display_links = ('student_id', 'name')

    # ডানপাশে ফিল্টারিং করার অপশন
    list_filter = ('status', 'course', 'batch', 'gender', 'blood_group', 'submitted_at')

    # ... (বাকি কোড অপরিবর্তিত থাকবে)

    # সার্চ বক্সের মাধ্যমে যা যা লিখে খোঁজা যাবে
    search_fields = ('student_id', 'name', 'phone', 'email', 'national_id_no')

    # সহজে অ্যাডমিন থেকেই স্ট্যাটাস পরিবর্তন করার সুবিধা
    list_editable = ('status',)

    # ফর্মের ফিল্ডগুলোকে সুন্দর করে ক্যাটাগরি অনুযায়ী সাজানো (Fieldsets)
    fieldsets = (
        ('Relations & Settings', {
            'fields': ('account', 'course', 'batch', 'status')
        }),
        ('Basic Information', {
            'fields': ('student_id', 'name', 'phone', 'email', 'gender', 'photo', 'admission_date')
        }),
        ('Address Details', {
            'fields': ('village_house_area', 'thana_upazila', 'district_city', 'post_code'),
            'classes': ('collapse',), # চাইলে এই সেকশনটি ডিফল্টভাবে হাইড করে রাখা যাবে
        }),
        ('Personal Information', {
            'fields': (
                'date_of_birth', 'marital_status', 'birth_certificate_no',
                'national_id_no', 'religion', 'blood_group'
            )
        }),
        ('Guardian Information', {
            'fields': ('father_name', 'father_phone', 'father_occupation', 'mother_name', 'guardian_name', 'guardian_phone')
        }),
        ('Academic Information', {
            'fields': (
                'education_institute_name', 'last_educational_qualification',
                'examination', 'passing_year', 'board_name', 'roll', 'registration_number'
            )
        }),
        ('Attachments & Checklists', {
            'fields': (
                'has_admission_form', 'has_passport_photo',
                'has_nid_photocopy', 'has_birth_certificate', 'has_marksheet_photocopy'
            )
        }),
        ('Signatures & Comments', {
            'fields': ('student_signature', 'authority_signature', 'authority_comments')
        }),
        ('System Metadata', {
            'fields': ('session', 'submitted_at'),
        }),
    )

    # readonly_fields যাতে submitted_at ফিল্ডটি ফর্মে দেখা যায় (যেহেতু এটি auto_now_add)
    readonly_fields = ('submitted_at',)
