# Generated by Django 3.2 on 2023-08-03 09:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230724_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления в минутах'),
        ),
    ]