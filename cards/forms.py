from django import forms

from .models import *


class CardDeckForm(forms.ModelForm):
    class Meta:
        model = CardDeck
        fields = [
            'name',
            'description',
            'lesson',
            'tags',
            'is_visible',
            'unlock_password'
        ]


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            'term',
            'definition'
        ]