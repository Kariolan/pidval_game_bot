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
    )
    stats = models.OneToOneField(
        'Stats',
        verbose_name="Stats",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_player",
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
        related_name="%(class)s_in_basement",
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
        max_length=64,
    )
    type = models.ForeignKey(
        'Type',
        verbose_name="Type",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_items",
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
        max_length=64,
    )
    decoration = models.ForeignKey(
        'Decoration',
        verbose_name="Decoration",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_on_position",
    )


class Decoration(models.Model):
    id = models.PositiveIntegerField(
        verbose_name="id",
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="Name",
        max_length=64,
    )
    type = models.ForeignKey(
        'Type',
        verbose_name="Type",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_decorations",
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
        max_length=64,
    )
    type = models.ForeignKey(
        'Type',
        verbose_name="Type",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_events",
    )
    description = models.TextField(
        verbose_name='Description'
    )
    results = models.ManyToManyField(
        'EventResult',
        verbose_name="Results",
        blank=True,
        related_name="%(class)s_results",
    )


class Type(models.Model):
    id = models.PositiveIntegerField(
        verbose_name="id",
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="Name",
        max_length=64,
    )


class EventResult(models.Model):
    name = models.CharField(
        verbose_name="Name",
        max_length=64,
    )
    probability = models.FloatField(
        verbose_name="Probability",
    )
    item = models.OneToOneField(
        'Item',
        verbose_name="Item Found",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
