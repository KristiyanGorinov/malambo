from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user-home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.groups.exists():
                group_names = [group.name for group in request.user.groups.all()]
                if any(group in allowed_roles for group in group_names):
                    return view_func(request, *args, **kwargs)

            return HttpResponse("You are not allowed to access this page.")
        return wrapper_func
    return decorator


class AllowedUsersMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        if request.user.groups.exists():
            group_names = [group.name for group in request.user.groups.all()]
            if any(group in self.allowed_roles for group in group_names):
                return super().dispatch(request, *args, **kwargs)

        return HttpResponse("You are not allowed to access this page.")