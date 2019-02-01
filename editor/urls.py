from django.urls import path

from . import views

app_name = 'editor'
urlpatterns = [
    path('', views.EditorView.as_view(), name='home'),
]
