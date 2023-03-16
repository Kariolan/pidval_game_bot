# Generated by Django 4.1.5 on 2023-03-16 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0013_remove_eventresult_item_eventresult_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='armor',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Armor'),
        ),
        migrations.AddField(
            model_name='stats',
            name='intelligence',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Intelligence'),
        ),
        migrations.AddField(
            model_name='stats',
            name='luck',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Luck'),
        ),
        migrations.AddField(
            model_name='stats',
            name='mental',
            field=models.IntegerField(blank=True, null=True, verbose_name='Mental'),
        ),
        migrations.AddField(
            model_name='stats',
            name='reaction',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Reaction'),
        ),
        migrations.AddField(
            model_name='stats',
            name='strength',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Energy'),
        ),
        migrations.AlterField(
            model_name='player',
            name='hryvni',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Hryvni'),
        ),
        migrations.AlterField(
            model_name='stats',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
    ]
