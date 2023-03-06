from django.contrib import admin

from .forms import PlayerForm
from .models import Message, Player, Basement, Stats, Item, Position, Decoration, Event, Type


@admin.register(Player)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'hostage', 'basement', 'inventory', 'stats', 'hryvni')
    form = PlayerForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')


@admin.register(Basement)
class BasementAdmin(admin.ModelAdmin):
    list_display = ('id', 'master', 'hostage', 'position')


@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    list_display = ('hp', 'energy')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'description')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'decoration')


@admin.register(Decoration)
class DecorationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'description')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'description')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
