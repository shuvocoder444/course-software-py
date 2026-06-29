from django.conf import settings
import json
from web_project.template_helpers.theme import TemplateHelper
from pathlib import Path
from django.contrib.auth.models import AnonymousUser

# রোলের ভিত্তিতে মেনু ফাইলের পাথ নির্ধারণ
def get_menu_file_path(role):
    # আপনার মডেলে থাকা রোলের সাথে মিল রেখে ম্যাপিং
    # মনে রাখবেন: মডেলে রোলগুলো বড় হাতের অক্ষরে আছে, তাই এখানেও সেভাবে হ্যান্ডেল করা ভালো
    filename_map = {
        "admin": "vertical_admin_menu.json",
        "teacher": "vertical_teacher_menu.json",
        "reception": "vertical_reception_menu.json",
        "accounts": "vertical_accounting_admin_menu.json",
        "student": "vertical_student_menu.json",
    }

    # রোলটিকে ছোট হাতের অক্ষরে রূপান্তর (যেমন: 'ADMIN' -> 'admin')
    role_key = str(role).lower()
    filename = filename_map.get(role_key, "vertical_menu.json")

    return Path(settings.BASE_DIR) / "templates" / "layout" / "partials" / "menu" / "vertical" / "json" / filename

class TemplateBootstrapLayoutVertical:
    @staticmethod
    def init(context):
        context.update({
            "layout": "vertical",
            "content_navbar": True,
            "is_navbar": True,
            "is_menu": True,
            "is_footer": True,
            "navbar_detached": True,
        })

        TemplateHelper.map_context(context)

        # ইউজার এবং রোল ডিটেকশন
        user = context.get("user")

        # যদি ইউজার লগইন করা থাকে এবং আমাদের কাস্টম Account মডেলের সাথে যুক্ত থাকে
        if user and not isinstance(user, AnonymousUser) and hasattr(user, "role"):
            role = user.role # আপনার মডেলের role ফিল্ড সরাসরি ব্যবহার করুন
        else:
            role = "student" # গেস্ট বা লগইন না করা ইউজারদের জন্য

        print(f"DEBUG: User: {user}, Role: {role}")

        # মেনু ডেটা ইনিশিয়ালাইজ করা
        TemplateBootstrapLayoutVertical.init_menu_data(context, role)
        return context

    @staticmethod
    def init_menu_data(context, role):
        menu_file_path = get_menu_file_path(role)
        try:
            with open(menu_file_path, 'r', encoding='utf-8') as file:
                context["menu_data"] = json.load(file)
        except FileNotFoundError:
            print(f"DEBUG: Menu file not found: {menu_file_path}")
            context["menu_data"] = [] # ফাইল না পেলে খালি লিস্ট
