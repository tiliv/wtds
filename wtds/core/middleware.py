class PjaxMiddleware(object):
    def process_request(self, request):
        request.is_pjax = lambda: request.META.get('HTTP_X_PJAX', False)
