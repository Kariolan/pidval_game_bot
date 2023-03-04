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


# class Master(models.Model):
#     master = models.ForeignKey(
#         to='test_app.Player',
#         verbose_name='Профіль гравця',
#         on_delete=models.PROTECT,
#     )
#     hostage = models.ForeignKey(
#         Player,
#         verbose_name='Заручник',
#         on_delete=models.CASCADE,
#     )
#
#     class Meta:
#         verbose_name = "Власник і заручник"
#         verbose_name_plural = "Власники і заручники"


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
