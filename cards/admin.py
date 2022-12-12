from django.contrib import admin

from .models import *


admin.site.register(CardDeck)
admin.site.register(Card)
admin.site.register(Question)
admin.site.register(Responce)