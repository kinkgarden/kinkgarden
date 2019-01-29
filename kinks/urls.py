from django.urls import path

from . import views

app_name = 'kinks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
