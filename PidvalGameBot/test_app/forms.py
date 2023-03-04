from django import forms

from .models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = {
            'external_id',
            'name',
            'hostage',
        }
        widget = {
            'name': forms.TextInput,
        }
