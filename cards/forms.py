from dataclasses import fields
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