from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("add/page", views.add, name="add"),
    path("edit/<str:entry>", views.edit, name="edit")
]
