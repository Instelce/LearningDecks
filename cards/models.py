import datetime
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db.models import Q


class CardDeckQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(name__icontains=query) | Q(description__icontains=query) | Q(lesson__icontains=query)
        return self.filter(lookups)


class CardDeckManager(models.Manager):
    def get_queryset(self):
        return CardDeckQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class CardDeck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=600)
    lesson = models.TextField(default="", blank=True)

    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()

    is_visible = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    unlock_password = models.IntegerField(default=0, blank=True)

    objects = CardDeckManager()

    def __str__(self):
        return f"{self.name} Deck - {self.user.username}"


class CardDeckFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(CardDeck, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username} like {self.deck.name} deck"


class Card(models.Model):
    deck = models.ForeignKey(CardDeck, on_delete=models.CASCADE)

    term = models.CharField(max_length=256)
    definition = models.TextField(max_length=600)

    def __str__(self):
        return f"{self.group.name} - {self.term} Card"


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(CardDeck, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    subject = models.CharField(max_length=300)
    content = models.TextField(max_length=600)

    def __str__(self) -> str:
        return f"Question of {self.user} about {self.subject}"


class Responce(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(CardDeck, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    content = models.TextField(max_length=600)
    rate = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Responce of {self.question.subject} of {self.user}"
