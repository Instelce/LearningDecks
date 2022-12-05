from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import context
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from taggit.models import Tag

from .models import *
from .forms import *


def home(request):
    return render(request, "cards/home.html", {})


def card_deck_list_view(request):
    card_decks = CardDeck.objects.filter(is_visible=True)

    if request.user:
        user_card_decks = CardDeck.objects.filter(user=request.user, is_visible=False)
    else:
        user_card_decks = None

    context = {
        'card_decks': card_decks,
        'user_card_decks': user_card_decks
    }
    return render(request, "cards/card_deck_list.html", context)    


def card_deck_tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    card_decks = CardDeck.objects.filter(tags=tag, is_visible=True) # Filter with tag
    context = {
        'tag': tag,
        'card_decks': card_decks
    }
    return render(request, "cards/card_deck_list.html", context)


def card_deck_detail_view(request, slug):
    card_deck = get_object_or_404(CardDeck, slug=slug)

    try:
        cards = Card.objects.filter(deck=card_deck)
    except Card.DoesNotExist:
        cards = None

    if request.POST and card_deck.user == request.user:
        card_form = CardForm(request.POST)
        if card_form.is_valid():
            new_card = card_form.save(commit=False)
            new_card.deck = card_deck
            new_card.save()
            return redirect('card-deck-detail', slug=slug)
    else:
        card_form = CardForm(request.POST)

    context = {
        "card_deck": card_deck,
        "card_form": card_form,
        "cards": cards
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
        return redirect(request.META.get('HTTP_REFERER'), '/')
    else:
        card_deck = get_object_or_404(CardDeck, slug=slug)
        if request.POST:
            card_deck.delete()
            messages.success(request, f"Deck has been deleted")
            return redirect('card-deck-list')
        return render(request, "cards/card_deck_delete.html", {})