from functools import wraps

from django.http import HttpResponseForbidden


def user_has_permission(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if any(role in allowed_roles for role in user.groups.values_list('name', flat=True)):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
        return _wrapped_view
    return decorator
