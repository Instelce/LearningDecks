import datetime
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class CardGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=600)
    lesson = models.TextField(default="")

    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    
    visibility = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    unlock_password = models.IntegerField(max_length=8, default=0)

    def __str__(self):
        return f"{self.name} Group - {self.user.username}"
    

class Card(models.Model):
    group = models.ForeignKey(CardGroup, on_delete=models.CASCADE)

    term = models.CharField(max_length=256)
    definition = models.TextField(max_length=600)
    favorite = models.BooleanField(default=False)
    is_learned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group.name} - {self.term} Card"
    


    