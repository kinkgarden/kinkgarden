from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404

from .models import KinkCategory, Kink


def index(request):
    category_list = KinkCategory.objects.order_by('name')
    context = {
        'category_list': category_list,
    }
    return render(request, 'kinks/index.html', context)


def category_detail(request, category_id):
    category = get_object_or_404(KinkCategory, pk=category_id)
    context = {
        'category': category,
        'kinks': category.kink_set.order_by('name'),
    }
    return render(request, 'kinks/category.html', context)


def detail(request, kink_id):
    kink = get_object_or_404(Kink, pk=kink_id)
    context = {
        'kink': kink,
    }
    return render(request, 'kinks/kink.html', context)
