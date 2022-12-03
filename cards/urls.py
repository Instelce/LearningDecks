from django.urls import path

from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("card-groups/", CardGroupListView.as_view(), name="card-group-list"),
    path("create-card-group/", card_group_create_view, name="card-group-create")
]
