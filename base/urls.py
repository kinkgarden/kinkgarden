from django.urls import path

from . import views

app_name = 'base'
urlpatterns = [
    path('', views.home_or_list_view, name='home'),
]
