from django.db import models
from foodgram.settings import PROJECT_CONSTANTS


class Tag(models.Model):
    """Ярлыки, задаётся админом."""

    name = models.CharField(
        max_length=PROJECT_CONSTANTS["LENGTH_TAG_NAME"],
        unique=True,
        verbose_name='Имя ярлыка',
    )
    color = models.CharField(
        max_length=PROJECT_CONSTANTS["LENGTH_HEX_COLOR"],
        unique=True,
        verbose_name='Цвет (HEX code)',
        default="#18c4e8",
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Ярлык")

    class Meta:
        verbose_name = "Ярлык"
        verbose_name_plural = "Ярлыки"

    def __str__(self):
        return self.slug
