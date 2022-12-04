from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from taggit.models import Tag

from .models import *
from .forms import *


def home(request):
    return render(request, "cards/home.html", {})


class CardDeckListView(ListView):
    model = CardDeck
    template_name = "cards/card_deck_list.html"
    context_object_name = 'card_decks'


def card_deck_tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    card_decks = CardDeck.objects.filter(tags=tag) # Filter with tag
    context = {
        'tag': tag,
        'card_decks': card_decks
    }
    return render(request, "cards/card_deck_list.html", context)


def card_deck_detail_view(request, slug):
    context = {
        "card_deck": CardDeck.objects.get(slug=slug)
    }
    return render(request, "cards/card_deck_detail.html", context)


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


@login_required
def card_deck_update_view(request, slug):
    if not CardDeck.objects.filter(user=request.user, slug=slug).exists():
        messages.error(request, f"You can't update this deck !")
        return redirect('card-deck-list')
    else:
        card_deck = get_object_or_404(CardDeck, slug=slug)

        form = CardDeckFrom(request.POST or None, instance=card_deck)
        if form.is_valid():
            form.save()
            messages.success(request, f"Deck has been updated")
            return redirect('card-deck-list')

        return render(request, "cards/card_deck_update.html", {"form": form})


@login_required
def card_deck_delete_view(request, slug):
    if not CardDeck.objects.filter(user=request.user, slug=slug).exists():
        messages.error(request, f"You can't delete this deck !")
        return redirect('card-deck-list')
    else:
        card_deck = get_object_or_404(CardDeck, slug=slug)
        if request.POST:
            card_deck.delete()
            messages.success(request, f"Deck has been deleted")
            return redirect('card-deck-list')
        return render(request, "cards/card_deck_delete.html", {})