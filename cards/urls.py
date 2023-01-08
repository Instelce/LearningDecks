from django.urls import path

from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("decks/", card_deck_list_view, name="card-deck-list"),
    path("decks/tag/<slug>/", card_deck_tagged, name="card-deck-tagged"),
    path("create-deck/", card_deck_create_view, name="card-deck-create"),
    path("decks/<slug>/", card_deck_detail_view, name="card-deck-detail"),
    path("decks/<slug>/learn/", card_deck_learning_view, name="card-deck-learning"),
    path("decks/<slug>/update/", card_deck_update_view, name="card-deck-update"),
    path("decks/<slug>/delete/", card_deck_delete_view, name="card-deck-delete"),
    path("decks/<deck_slug>/cards/<card_id>/update/", card_update_view, name="card-update"),
    path("decks/<deck_slug>/cards/<card_id>/delete/", card_delete_view, name="card-delete"),

    path("decks/<deck_slug>/questions/", card_deck_question_list_view, name="card-deck-question-list"),
]
