from django.shortcuts import render

from kinks.models import Kink


def home_view(request):
    kink_count = Kink.objects.count()
    return render(request, 'base/index.html', {'kink_count': kink_count})
