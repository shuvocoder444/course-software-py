from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

class CourseView(TemplateView):
    # আপনার দেওয়া পাথ অনুযায়ী টেমপ্লেটের নাম (অ্যাপের templates ফোল্ডারের ভেতরের পাথ)
    template_name = "courses.html"

    # Predefined function to initialize layout context
    def get_context_data(self, **kwargs):
        # গ্লোবাল লেআউট ইনিট করা (web_project/__init__.py থেকে)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # vertical layout সেট করা হলো
        context.update(
            {
                "layout": "vertical",
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            }
        )

        return context
