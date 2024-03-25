from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def member_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_member:
            # Redirect to member login if not authenticated or not a member
            login_url = reverse('members:login')
            return redirect(login_url)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
