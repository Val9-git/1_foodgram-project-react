# Generated by Django 3.2 on 2023-07-19 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Имя ярлыка')),
                ('color', models.CharField(default='#18c4e8', max_length=7, unique=True, verbose_name='Цвет (HEX code)')),
                ('slug', models.SlugField(unique=True, verbose_name='Ярлык')),
            ],
            options={
                'verbose_name': 'Ярлык',
                'verbose_name_plural': 'Ярлыки',
            },
        ),
    ]
