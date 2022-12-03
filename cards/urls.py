from django.urls import path

from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("decks/", CardDeckListView.as_view(), name="card-deck-list"),
    path("create-deck/", card_deck_create_view, name="card-deck-create")
]
