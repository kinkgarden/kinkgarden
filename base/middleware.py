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


class AgeGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        return self.get_response(request)

    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs):
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
        response: HttpResponse = redirect(request.path_info)
        response.set_cookie("age-gate-accepted", "yes", max_age=999999999)
        return response
