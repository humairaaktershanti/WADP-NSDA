from django.shortcuts import redirect
from adminApp.models import *
from functools import wraps

def block_after_resignation(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if profile:
            resignation = ResignationModel.objects.filter(employee=profile, status='approved').first()
            if resignation:
                # Allow access only to employee_profile or employee_certificate
                if request.path not in [f'/employee_profile/', f'/employee_certificate/{profile.id}/']:
                    return redirect('employee_profile')
        return view_func(request, *args, **kwargs)
    return _wrapped_view