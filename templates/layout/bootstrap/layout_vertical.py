from django.conf import settings
import json
from web_project.template_helpers.theme import TemplateHelper
from pathlib import Path
from django.contrib.auth.models import AnonymousUser

# রোলের ভিত্তিতে মেনু ফাইলের পাথ নির্ধারণ
def get_menu_file_path(role):
    filename_map = {
        "admin": "vertical_admin_menu.json",
        "teacher": "vertical_teacher_menu.json",
        "reception": "vertical_reception_menu.json",
        "accounts": "vertical_accounting_admin_menu.json",
        "student": "vertical_student_menu.json",
    }

    # রোলটিকে ছোট হাতের অক্ষরে রূপান্তর ও এক্সট্রা স্পেস বাদ দেওয়া
    role_key = str(role).lower().strip()
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
        role = "student"  # ডিফল্ট রোল

        if user and not isinstance(user, AnonymousUser) and hasattr(user, "role"):
            role = user.role

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
            # প্রোডাকশনে ক্র্যাশ এড়াতে ফাইল না পাওয়া গেলে খালি লিস্ট সেট হবে
            context["menu_data"] = []
