from django.db import models


# Гравець
class Player(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID гравця',
        unique=True,
    )
    name = models.TextField(
        verbose_name="Ім'я гравця",
    )
    hostage = models.ForeignKey(
        'Player',
        verbose_name="Заручник",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    basement = models.ForeignKey(
        'Basement',
        verbose_name="Basement",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_player",
    )
    inventory = models.ManyToManyField(
        'Item',
        verbose_name="Inventory",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    stats = models.OneToOneField(
        'Stats',
        verbose_name="Stats",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)_player",
    )
    hryvni = models.IntegerField(
        verbose_name="Hryvni",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = "Профіль гравця"
        verbose_name_plural = "Профілі гравців"


class Message(models.Model):
    profile = models.ForeignKey(
        to='test_app.Player',
        verbose_name='Профіль гравця',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Час отримання',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Повідомлення {self.pk} від {self.profile}'

    class Meta:
        verbose_name = 'Повідомлення'
        verbose_name_plural = 'Повідомлення'


class Basement(models.Model):
    id = models.PositiveIntegerField(
        verbose_name="id",
        unique=True,
        primary_key=True,
    )
    master = models.OneToOneField(
        'Player',
        verbose_name="Master",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_master",
    )
    hostage = models.OneToOneField(
        'Player',
        verbose_name="Hostage",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_hostage",
    )
    position = models.ManyToManyField(
        'Position',
        verbose_name="Position",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)_in_basement",
    )


class Stats(models.Model):
    hp = models.PositiveIntegerField(
        verbose_name="HP",
        blank=True,
        null=True,
    )
    energy = models.PositiveIntegerField(
        verbose_name="Energy",
        blank=True,
        null=True,
    )


class Item(models.Model):
    id = models.PositiveIntegerField(
        verbose_name="id",
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="Name",
    )
    type = models.ForeignKey(
        'Type',
        verbose_name="Type",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="Items_%(class)",
    )
    description = models.TextField(
        verbose_name='Description'
    )


class Position(models.Model):
    id = models.PositiveIntegerField(
        verbose_name="id",
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="Name",
    )
    decoration = models.ForeignKey(
        'Decoration',
        verbose_name="Decoration",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)_on_position",
    )


class Decoration(models.Model):
    id = models.PositiveIntegerField(
        verbose_name="id",
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="Name",
    )
    type = models.ForeignKey(
        'Type',
        verbose_name="Type",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="Decorations_%(class)",
    )
    description = models.TextField(
        verbose_name='Description'
    )


class Event(models.Model):
    id = models.PositiveIntegerField(
        verbose_name="id",
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="Name",
    )
    type = models.ForeignKey(
        'Type',
        verbose_name="Type",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="Events_%(class)",
    )
    description = models.TextField(
        verbose_name='Description'
    )


class Type(models.Model):
    id = models.PositiveIntegerField(
        verbose_name="id",
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="Name",
    )
