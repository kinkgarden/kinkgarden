import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

from .models import KinkCategory, Kink


class IndexView(generic.ListView):
    template_name = 'kinks/index.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return KinkCategory.objects.order_by('name')

    def render_to_response(self, context, **response_kwargs):
        if self.request.META['HTTP_ACCEPT'] == 'application/json':
            return JsonResponse(
                {
                    'categories': list(KinkCategory.objects.values()),
                    'kinks': list(Kink.objects.values()),
                },
                **response_kwargs
            )
        else:
            return super().render_to_response(context, **response_kwargs)


class CategoryView(generic.DetailView):
    model = KinkCategory
    context_object_name = 'category'
    template_name = 'kinks/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kinks'] = context['category'].kink_set.order_by('name')
        return context


class DetailView(generic.DetailView):
    model = Kink
    template_name = 'kinks/kink.html'


class KinkColumn:
    def __init__(self, name, kinks):
        self.name = name
        self.kinks = kinks

    @classmethod
    def deserialize_all(cls, columns):
        all_ids = set(id for column in columns for id in column[1:])
        all_kinks = Kink.objects.filter(id__in=all_ids)
        all_kinks = dict((x.id, x) for x in all_kinks)

        def deserialize(column):
            name, *ids = column
            kinks = [all_kinks[x] for x in ids if x in all_kinks]
            return cls(name, kinks)

        return [deserialize(column) for column in columns]


def kink_list_view(request):
    if len(request.GET) != 1:
        raise TypeError()
    list_data = list(request.GET.keys())[0]
    try:
        list_data = json.loads(list_data)
    except json.JSONDecodeError:
        raise TypeError()
    try:
        columns = KinkColumn.deserialize_all(list_data)
    except ValueError:
        raise TypeError()
    return render(request, 'kinks/list.html', {'columns': columns})
