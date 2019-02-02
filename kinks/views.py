from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.http import JsonResponse

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
