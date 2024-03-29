from django.urls import path

from . import views

app_name = "kinks"
urlpatterns = [
    path("<uuid:pk>", views.KinkListView.as_view(), name="kink_list"),
    path("new", views.KinkListCreate.as_view(), name="kink_list_new"),
    path("<uuid:pk>/edit", views.KinkListEdit.as_view(), name="kink_list_edit"),
    path("<uuid:pk>/save", views.KinkListSave.as_view(), name="kink_list_save"),
    path("patreon/redirect", views.PatreonRedirect.as_view(), name="patreon_redirect"),
    path(
        "<slug:short_link>",
        views.KinkListView.as_view(),
        name="kink_list_by_short_link",
    ),
]
