from django.urls import path

from . import views

app_name = 'kinks'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_detail, name='category'),
    path('<int:kink_id>/', views.detail, name='detail'),
]
