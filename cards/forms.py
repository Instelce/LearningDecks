from dataclasses import fields
from django import forms

from .models import *


class CardDeckCheckAccessForm(forms.Form):
    unlock_password = forms.CharField(required=True)


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


class CardDeckFavoriteForm(forms.ModelForm):
    class Meta:
        model = CardDeckFavorite
        fields = []


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            'term',
            'definition'
        ]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'subject',
            'content'
        ]


class ResponceForm(forms.ModelForm):
    class Meta:
        model = Responce
        fields = [
            'content',
            'rate'
        ]