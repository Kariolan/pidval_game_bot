# Generated by Django 4.1.5 on 2023-03-10 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0012_alter_basement_id_alter_decoration_id_alter_event_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventresult',
            name='item',
        ),
        migrations.AddField(
            model_name='eventresult',
            name='item',
            field=models.ManyToManyField(blank=True, to='test_app.item', verbose_name='Item Found'),
        ),
    ]
