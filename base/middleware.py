from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from .views import age_gate_view


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
        if request.COOKIES.get("age-gate-accepted", "") != "yes":
            age_gate_response = age_gate_view(request)
            if age_gate_response is not None:
                return age_gate_response
            response: HttpResponse = self.get_response(request)
            response.set_cookie("age-gate-accepted", "yes", max_age=999999999)
            return response
        else:
            return self.get_response(request)
