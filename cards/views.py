from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.template.defaultfilters import slugify

from .models import *
from .forms import *


def home(request):
    return render(request, "cards/home.html", {})


class CardGroupListView(ListView):
    model = CardGroup
    template_name = "cards/card_group_list.html"
    context_object_name = 'card_groups'


def card_group_create_view(request):
    form = CardGroupFrom(request.POST or None)
    if form.is_valid():
        new_card_group = form.save(commit=False)
        new_card_group.user = request.user
        new_card_group.slug = slugify(new_card_group.name)
        new_card_group.save()
        form.save_m2m()
    return render(request, 'cards/card_group_create.html', {'form': form})
