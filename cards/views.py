from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import *


def home(request):
    return render(request, "cards/home.html", {})


class CardDeckListView(ListView):
    model = CardDeck
    template_name = "cards/card_deck_list.html"
    context_object_name = 'card_decks'


@login_required
def card_deck_create_view(request):
    if request.POST:
        form = CardDeckFrom(request.POST)
        if form.is_valid():
            new_card_deck = form.save(commit=False)
            new_card_deck.user = request.user
            new_card_deck.slug = slugify(new_card_deck.name)
            new_card_deck.save()
            form.save_m2m()
            messages.success(request, f"Deck has been created")
            return redirect('card-deck-list')
    else:
        form = CardDeckFrom()
    return render(request, 'cards/card_deck_create.html', {'form': form})
