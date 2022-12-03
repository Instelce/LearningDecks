from django import forms

from .models import *


class CardDeckFrom(forms.ModelForm):
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