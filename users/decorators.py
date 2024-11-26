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

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allowed to access this page.")
        return wrapper_func
    return decorator

#for CBV

class AllowedUsersMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponse("You are not allowed to access this page.")