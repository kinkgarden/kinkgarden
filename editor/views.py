from django.views import generic


class EditorView(generic.TemplateView):
    template_name = "editor/editor.html"
