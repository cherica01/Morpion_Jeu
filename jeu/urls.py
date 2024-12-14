from django.urls import path
from . import views

urlpatterns = [
    path("", views.jeu_morpion, name="jeu_morpion"),
]
