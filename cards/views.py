from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import context
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from taggit.models import Tag
from hitcount.views import HitCountDetailView


from .models import *
from .forms import *


def home(request):
    return render(request, "cards/home.html", {})


# Dashboard
def dashboard(request):
    user_card_decks = CardDeck.objects.filter(user=request.user)
    context = {
        'card_decks': user_card_decks
    }
    return render(request, "cards/dashboard.html", context)


# Card Deck Views (list, tagged, create, update, delete)
def card_deck_list_view(request):
    # All visible card decks
    query = request.GET.get('search')
    print(query, len(str(query)))
    if query is not None and len(str(query)) != 0:
        card_decks = CardDeck.objects.filter(is_visible=True).search(query=query).order_by("-created_at")
    else:
        card_decks = CardDeck.objects.filter(is_visible=True).order_by("-created_at")

    if request.user.is_authenticated:
        # User card decks
        user_card_decks = CardDeck.objects.filter(user=request.user, is_visible=False).order_by("-created_at")
    else:
        user_card_decks = None

    # Favorite
    card_deck_favorites = []
    for deck in CardDeck.objects.all():
        deck_favorite = [deck.slug, 0, False]
        for favorite in CardDeckFavorite.objects.all():
            if favorite.deck == deck:
                deck_favorite[1] += 1
                if request.user.is_authenticated:
                    if favorite.user == request.user:
                        deck_favorite[2] = True
                    else:
                        deck_favorite[2] = False

        card_deck_favorites.append((deck_favorite))

    # Card in card deck
    cards_in_card_decks = []
    for deck in CardDeck.objects.all():
        cards = [deck.slug, 0]
        for card in Card.objects.all():
            if card.deck == deck:
                cards[1] += 1
        cards_in_card_decks.append(cards)

    context = {
        'card_decks': card_decks,
        'user_card_decks': user_card_decks,
        'card_deck_favorites': card_deck_favorites,
        'cards_in_card_decks': cards_in_card_decks,
    }
    return render(request, "cards/card_deck_list.html", context)


def card_deck_tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    card_decks = CardDeck.objects.filter(tags=tag, is_visible=True).order_by("-created_at") # Filter with tag
    if request.user.is_authenticated:
        user_card_decks = CardDeck.objects.filter(tags=tag, user=request.user, is_visible=False).order_by("-created_at")
    else:
        user_card_decks = None

    context = {
        'tag': tag,
        'card_decks': card_decks,
        'user_card_decks': user_card_decks
    }
    return render(request, "cards/card_deck_list.html", context)


def card_deck_learning_view(request, slug):
    card_deck = get_object_or_404(CardDeck, slug=slug)

    # Get cards of card deck
    try:
        cards = Card.objects.filter(deck=card_deck)
    except Card.DoesNotExist:
        cards = None

    context = {
        "card_deck": card_deck,
        "cards": cards
    }
    return render(request, "cards/card_deck_learning.html", context)


def card_deck_detail_check_access(request, slug):
    card_deck = CardDeck.objects.get(slug=slug)

    if request.POST:
        form = CardDeckCheckAccessForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['unlock_password'] == card_deck.unlock_password:
                return redirect('card_deck_detail', slug=slug)
    else:
        form = CardDeckCheckAccessForm()

    context = {
        'card_deck': card_deck,
        'form': form
    }

    return render(request, "card_deck_detail_check_access.html", context)


def card_deck_detail_view(request, slug):
    card_deck = get_object_or_404(CardDeck, slug=slug)

    # Get cards of card deck
    try:
        cards = Card.objects.filter(deck=card_deck)
    except Card.DoesNotExist:
        cards = None

    # Create card form if user owned the deck
    if 'create-card' in request.POST and card_deck.user == request.user:
        card_form = CardForm(request.POST)
        if card_form.is_valid():
            new_card = card_form.save(commit=False)
            new_card.deck = card_deck
            new_card.save()
            return redirect('card-deck-detail', slug=slug)
    else:
        card_form = CardForm(request.POST)

    # Check and get the card deck favorite
    if request.user.is_authenticated:
        try:
            card_deck_favorite = CardDeckFavorite.objects.get(user=request.user, deck=card_deck)
        except CardDeckFavorite.DoesNotExist:
            card_deck_favorite = None
    else:
        card_deck_favorite = None

    # Add favorite form
    if 'add-favorite' in request.POST and request.user.is_authenticated:
        card_deck_favorite_form = CardDeckFavoriteForm(request.POST)
        if card_deck_favorite_form.is_valid():
            new_favorite = card_deck_favorite_form.save(commit=False)
            new_favorite.deck = card_deck
            new_favorite.user = request.user
            new_favorite.save()
            return redirect('card-deck-detail', slug=slug)
    else:
        card_deck_favorite_form = CardDeckFavoriteForm(request.POST)

    # Remove favorite form
    if 'remove-favorite' in request.POST and request.user.is_authenticated:
        card_deck_favorite.delete()
        return redirect('card-deck-detail', slug=slug)
    else:
        card_deck_favorite_form = CardDeckFavoriteForm()

    card_deck_favorite_count = CardDeckFavorite.objects.filter(deck=card_deck).count()

    cards_in_card_decks = 0
    for card in Card.objects.all():
        if card.deck == card_deck:
            cards_in_card_decks += 1

    context = {
        "card_deck": card_deck,
        "card_form": card_form,
        "cards": cards,
        "card_deck_favorite_form": card_deck_favorite_form,
        "card_deck_favorite": card_deck_favorite,
        "card_deck_favorite_count": card_deck_favorite_count,
        "cards_in_card_decks": cards_in_card_decks
    }
    return render(request, "cards/card_deck_detail.html", context)


class CardDeckHitCountView(HitCountDetailView):
    model = CardDeck
    template_name = 'cards/card_deck_hit_count.html'
    count_hit = True
 
    def get_context_data(self, **kwargs):
        context = super(CardDeckHitCountView, self).get_context_data(**kwargs)
        context.update({
        })
        self.object = self.get_object()
        return context


@login_required
def card_deck_create_view(request):
    if request.POST:
        form = CardDeckForm(request.POST)
        if form.is_valid():
            new_card_deck = form.save(commit=False)
            new_card_deck.user = request.user
            new_card_deck.slug = slugify(new_card_deck.name)
            new_card_deck.save()
            form.save_m2m()
            messages.success(request, f"{new_card_deck.name.capitalize()} deck has been created")
            return redirect('card-deck-list')
    else:
        form = CardDeckForm()
    return render(request, 'cards/card_deck_create.html', {'form': form})


@login_required
def card_deck_update_view(request, slug):
    # Checks if the connected user is the owner of the deck
    if not CardDeck.objects.filter(user=request.user, slug=slug).exists():
        messages.error(request, f"You can't update this deck !")
        return redirect('card-deck-list')
    else:
        card_deck = get_object_or_404(CardDeck, slug=slug)

        form = CardDeckForm(request.POST or None, instance=card_deck)
        if form.is_valid():
            messages.success(request, f"{card_deck.name.capitalize()} deck has been updated")
            form.save()
            return redirect('card-deck-detail', slug=card_deck.slug)

        return render(request, "cards/card_deck_update.html", {"form": form})


@login_required
def card_deck_delete_view(request, slug):
    # Checks if the connected user is the owner of the deck
    if not CardDeck.objects.filter(user=request.user, slug=slug).exists():
        messages.error(request, f"You can't delete this deck !")
        return redirect(request.META.get('HTTP_REFERER'), '/')
    else:
        card_deck = get_object_or_404(CardDeck, slug=slug)
        if request.POST:
            messages.success(request, f"{card_deck.name.capitalize()} deck has been deleted")
            card_deck.delete()
            return redirect('card-deck-list')
        return render(request, "cards/card_deck_delete.html", {'card_deck': card_deck})


# Card Views (update, delete)
@login_required
def card_update_view(request, deck_slug, card_id):
    # Checks if the connected user is the owner of the card's deck
    if not CardDeck.objects.filter(user=request.user, slug=deck_slug).exists():
        messages.error(request, f"You can't update this card, you are not the owner of the card deck !")
        return redirect('card-deck-detail', slug=deck_slug)
    else:
        card = get_object_or_404(Card, id=card_id)
        form = CardForm(request.POST or None, instance=card)
        if form.is_valid():
            messages.success(request, f"{card.term.capitalize()} card has been updated")
            form.save()
            return redirect('card-deck-detail', slug=deck_slug)

        return render(request, "cards/card_update.html", {"form": form})


@login_required
def card_delete_view(request, deck_slug, card_id):
    # Checks if the connected user is the owner of the card's deck
    if not CardDeck.objects.filter(user=request.user, slug=deck_slug).exists():
        messages.error(request, f"You can't delete this card, you are not the owner of the card deck !")
        return redirect('card-deck-detail', slug=deck_slug)
    else:
        card = get_object_or_404(Card, id=card_id)
        if request.POST:
            messages.success(request, f"{card.term.capitalize()} card has been deleted")
            card.delete()
            return redirect('card-deck-detail', slug=deck_slug)
        return render(request, "cards/card_delete.html", {'card': card})


# Questions and responces views
@login_required
def card_deck_question_list_view(request, deck_slug):
    card_deck = get_object_or_404(CardDeck, slug=deck_slug)
    questions = Question.objects.filter(deck=card_deck).order_by('-created_at')
    responces = Responce.objects.filter(deck=card_deck)

    # Question
    if 'post-question' in request.POST:
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            new_question = question_form.save(commit=False)
            new_question.user = request.user
            new_question.deck = card_deck
            new_question.save()
            return redirect('card-deck-question-list', deck_slug=deck_slug)
    else:
        question_form = QuestionForm()

    # Responce
    if 'post-responce' in request.POST:
        responce_form = ResponceForm(request.POST)
        if responce_form.is_valid():
            question_id = responce_form.cleaned_data['responce-question']
            new_responce = responce_form.save(commit=False)
            new_responce.user = request.user
            new_responce.deck = card_deck
            new_responce.question = Question.objects.get(id=question_id)
            new_responce.save()
            return redirect('card-deck-question-list', deck_slug=deck_slug)
    else:
        responce_form = ResponceForm()

    context = {
        'card_deck': card_deck,
        'questions': questions,
        'question_form': question_form,
        'responces': responces,
        'responce_form': responce_form,
    }

    return render(request, "cards/card_deck_question_list.html", context)
