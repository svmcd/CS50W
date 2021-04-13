from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("wiki/<str:title>", views.wiki_title, name="title"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random")
]
