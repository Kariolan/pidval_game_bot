from django.contrib import admin

from .forms import PlayerForm
from .models import Message
from .models import Player


@admin.register(Player)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'hostage')
    form = PlayerForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')
