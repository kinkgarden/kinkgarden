from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import generic

from kinks.models import Kink, KinkList


def home_view(request):
    kink_count = Kink.objects.count()
    list_count = KinkList.objects.count()
    try:
        random_example = KinkList.objects.filter(example=True).order_by('?')[0:1].get()
    except KinkList.DoesNotExist:
        random_example = None
    return render(request, 'base/index.html', {'kink_count': kink_count, 'list_count': list_count, 'example': random_example})


class PrivacyPolicyView(generic.TemplateView):
    template_name = 'base/privacy_policy.html'


def age_gate_view(request: HttpRequest):
    if 'age-gate-accept' in request.POST:
        return None
    if 'age-gate-reject' in request.POST:
        return redirect('https://example.com')
    return render(request, 'base/age-gate.html')
