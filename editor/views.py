from django.views import generic

from kinks.models import KinkCategory, Kink


class EditorView(generic.TemplateView):
    template_name = "editor/editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = {
            'categories': list(KinkCategory.objects.values()),
            'kinks': list(Kink.objects.values()),
        }
        return context
