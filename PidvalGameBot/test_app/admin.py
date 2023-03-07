from django.contrib import admin

from .forms import PlayerForm
from .models import * #Message, Player, Basement, Stats, Item, Position, Decoration, Event, Type


@admin.register(Player)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'hostage', 'basement', 'get_inventory', 'stats', 'hryvni')
    form = PlayerForm

    def get_inventory(self, obj):
        return "\n".join([p.inventory for p in obj.inventory.all()])


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')


@admin.register(Basement)
class BasementAdmin(admin.ModelAdmin):
    list_display = ('id', 'master', 'hostage', 'get_position')

    def get_position(self, obj):
        return "\n".join([p.position for p in obj.position.all()])


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

@admin.register(EventResult)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'probability')