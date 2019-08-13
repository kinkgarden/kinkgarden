import base64
from collections import namedtuple

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


def decode_one(data: bytes):
    """
    Decodes a single kink.
    :param data: the bytes to operate on
    :return: (column ID, custom?, intensity, id / text, remaining data)
    """
    header = data[:2]
    column = header[0] >> 6
    type = header[0] >> 5 & 0b1
    intensity = header[0] >> 3 & 0b11
    rest = (header[0] & 0b111) << 8 | header[1]
    if type == 0:
        return column, False, intensity, rest, data[2:]
    else:
        text = data[2:2 + rest].decode('utf-8')
        return column, True, intensity, text, data[2 + rest:]


def decode_all(data: bytes):
    """
    Decodes an entire set of kinks.
    :param data: bytes to operate on
    :return: a list of (column, custom?, intensity, id / text) tuples
    """
    result = []
    while len(data) > 0:
        column, custom, intensity, value, data = decode_one(data)
        result.append((column, custom, intensity, value))
    return result


ConcreteKink = namedtuple('ConcreteKink', ['name', 'description', 'intensity'])


def hydrate(data: bytes):
    decoded = decode_all(data)
    columns = [[], [], [], []]
    all_ids = set(value for (_, custom, _, value) in decoded if not custom)
    all_kinks = Kink.objects.filter(id__in=all_ids)
    all_kinks = dict((x.id, x) for x in all_kinks)
    for (column, custom, intensity, value) in decoded:
        if custom:
            name, description = value.split('\n', 1)
        else:
            kink = all_kinks[value]
            name, description = kink.name, kink.description
        hydrated = ConcreteKink(name, description, intensity)
        columns[column].append(hydrated)
    return columns


def kink_list_view(request):
    if len(request.GET) != 1:
        raise TypeError()
    list_data = list(request.GET.keys())[0]
    list_data = list_data.replace('!', '=')
    list_data = base64.b64decode(list_data)
    columns = hydrate(list_data)
    names = ["S tier", "good shit", "okay i guess", "nnnnnnope"]
    return render(request, 'kinks/list.html', {'columns': zip(names, columns)})
