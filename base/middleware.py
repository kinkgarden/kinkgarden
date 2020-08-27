from functools import wraps

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from . import views


class RTAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Rating"] = "RTA-5042-1996-1400-1577-RTA"
        return response


def ignore_age_gate(view_func):
    """Mark a view function as being exempt from the CSRF view protection."""
    # view_func.csrf_exempt = True would also work, but decorators are nicer
    # if they don't have side effects, so return a new function.
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.ignore_age_gate = True
    return wraps(view_func)(wrapped_view)


class AgeGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(view_func, "ignore_age_gate", False):
            return None
        if getattr(request, "age_gate_accepted", False):
            return None
        if request.COOKIES.get("age-gate-accepted", "") == "yes":
            return None
        age_gate_response = views.age_gate_view(request)
        if age_gate_response is not None:
            return age_gate_response
        request.age_gate_accepted = True
        response: HttpResponse = self.get_response(request)
        response.set_cookie("age-gate-accepted", "yes", max_age=999999999)
        return response
