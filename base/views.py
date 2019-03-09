from django.shortcuts import render
from django.views import generic

from kinks.models import Kink
from kinks.views import kink_list_view


def home_or_list_view(request):
    try:
        return kink_list_view(request)
    except TypeError:
        kink_count = Kink.objects.filter(custom__exact=False).count()
        return render(request, 'base/index.html', {'kink_count': kink_count})
