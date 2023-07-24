"""Для запуска программы введите команду 'python manage.py load_data'."""

import csv
import os

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from recipes.models import Ingredient

# TABLES = {
#     User: 'users.csv',
#     Category: 'category.csv',
#     Genre: 'genre.csv',
#     Title: 'titles.csv',
#     Review: 'review.csv',
#     Comment: 'comments.csv',
# }

DATA_PATH = os.path.join(settings.BASE_DIR, 'data')
INGREDIENTS_DATA = os.path.join(DATA_PATH, 'ingredients.csv')


class Command(BaseCommand):
    """Команда для импорта .csv файла в Базу Данных."""
    def handle(self, *args, **kwargs):
        try:
            with open(INGREDIENTS_DATA, 'r', encoding='UTF-8') as ingredients:
                data = csv.reader(ingredients)
                for fields in data:
                    name, measurement_unit = fields
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit,
                    )
        except FileNotFoundError:
            raise CommandError('Добавьте файл ingredients.csv'
                               'в директорию backend/data ')
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
