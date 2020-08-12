from django.shortcuts import render

from kinks.models import Kink, KinkList


def home_view(request):
    kink_count = Kink.objects.count()
    list_count = KinkList.objects.count()
    try:
        random_example = KinkList.objects.filter(example=True).order_by('?')[0:1].get()
    except KinkList.DoesNotExist:
        random_example = None
    return render(request, 'base/index.html', {'kink_count': kink_count, 'list_count': list_count, 'example': random_example})
