from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def admin_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            # Redirect to admin login if not authenticated or not an admin
            login_url = reverse('admins:admin_login')
            return redirect(login_url)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
