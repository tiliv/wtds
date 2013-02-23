from functools import wraps

from django.core.exceptions import PermissionDenied

from .models import Wallpaper

def requires_authorship(view_func):
    """ Checks that the Wallpaper specified by url kwarg ``pk`` is owned by the user.  """
    @wraps(view_func)
    def _check_authorship(self, request, *args, **kwargs):
        try:
            wallpaper = Wallpaper.objects.get(pk=kwargs['pk'])
        except Wallpaper.DoesNotExist:
            is_owned = False
        else:
            is_owned = wallpaper.uploader == request.user

        if request.user.is_active and (request.user.is_staff or is_owned):
            return view_func(self, request, *args, **kwargs)
        raise PermissionDenied
    return _check_authorship
