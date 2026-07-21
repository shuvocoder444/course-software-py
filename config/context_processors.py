from django.conf import settings

def my_setting(request):
    return {'MY_SETTING': settings}

def language_code(request):
    return {"LANGUAGE_CODE": request.LANGUAGE_CODE}

def get_cookie(request):
    return {"COOKIES": request.COOKIES}

# Add the 'ENVIRONMENT' setting to the template context
def environment(request):
    return {'ENVIRONMENT': settings.ENVIRONMENT}


from apps.setting.models import SiteSetting

def site_global_settings(request):
    # ডাটাবেজ থেকে সেটিংস ডাটা তুলে আনা
    settings = SiteSetting.objects.first()

    # যদি ডাটাবেজ একদম খালি থাকে, তাহলে এরর এড়াতে একটা ডিফল্ট অবজেক্ট তৈরি করে নিবে
    if not settings:
        settings = SiteSetting.objects.create()

    # print("a", settings)

    return {
        'global_settings': settings
    }
