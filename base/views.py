from django.views import generic

from kinks.models import Kink


class HomeView(generic.TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kink_count'] = Kink.objects.filter(custom__exact=False).count()
        return context
