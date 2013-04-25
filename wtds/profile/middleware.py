from .models import Profile

class ActiveProfileMiddleware(object):
    """ Fetches the currently activated profile in advance, to save redundant lookups. """
    def process_request(self, request):
        """ Sets an ``active_profile`` attribute on the current user. """
        request.user.active_profile = Profile.objects.get_active(user=request.user)
