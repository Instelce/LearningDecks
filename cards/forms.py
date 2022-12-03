from django import forms

from .models import *


class CardGroupFrom(forms.ModelForm):
    class Meta:
        model = CardGroup
        fields = [
            'name',
            'description',
            'lesson',
            'tags',
            'is_visible',
            'unlock_password'
        ]