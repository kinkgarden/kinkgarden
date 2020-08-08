from django.http import HttpResponse


class RTAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response: HttpResponse = self.get_response(request)
        response['Rating'] = 'RTA-5042-1996-1400-1577-RTA'

        # Code to be executed for each request/response after
        # the view is called.

        return response
