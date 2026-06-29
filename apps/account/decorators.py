from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            # request.user.role check করা হচ্ছে যা আপনার মডেলে আছে
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied  # সঠিক রোল না থাকলে সরাসরি 403 Forbidden দিবে
        return wrap
    return decorator
