from django.urls import path
from django.urls import reverse

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<entry_name>", views.entry_detail, name="entry_detail"),
    path("add/", views.add, name="add"),
    path("edit/<entry_name>", views.edit, name="edit"),
    path("delete/<entry_name>", views.delete, name="delete"),
    path("random", views.random_page, name="random")
]
