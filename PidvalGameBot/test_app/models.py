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
    # master = models.ForeignKey(
    #     'Player',
    #     verbose_name="Власник",
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )
    hostage = models.ForeignKey(
        'Player',
        verbose_name="Заручник",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
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
        verbose_name="Master",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_hostage",
    )