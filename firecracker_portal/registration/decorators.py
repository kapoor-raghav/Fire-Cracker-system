from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUserProfile
from django.shortcuts import get_object_or_404

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                messages.error(request, "You must be logged in.")
                return redirect('unauthorized')
            user = get_object_or_404(CustomUserProfile, id=user.id)
            role = getattr(user, 'role', None)
            if role not in allowed_roles:
                messages.error(request, "You do not have permission to access this page.")
                return redirect('unauthorized')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
