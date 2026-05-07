from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def role_required(required_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            try: # YOU DONT KNOW IF ITS THERE DO NOT FORGET!!!!!!!!!!!!!!!!!!!!!!
                profile = request.user.profile
            except:
                raise PermissionDenied

            if profile.role != required_role:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator