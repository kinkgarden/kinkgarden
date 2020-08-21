from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import ensure_csrf_cookie

from kinks.models import KinkCategory, Kink


@method_decorator(ensure_csrf_cookie, name="dispatch")
class EditorView(generic.TemplateView):
    template_name = "editor/editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["db_data"] = {
            "categories": list(KinkCategory.objects.values()),
            "kinks": list(Kink.objects.values()),
        }
        return context
