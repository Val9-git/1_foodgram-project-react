from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Спец модель Пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    GUEST = 'guest'
    AUTHORIZED = 'authorized'
    ADMIN = 'admin'

    ROLES = [
        (GUEST, 'guest'),
        (AUTHORIZED, 'authorized'),
        (ADMIN, 'Administrator'),
    ]

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        blank=False,
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        blank=False,
        max_length=150,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default='guest'
    )

    @property
    def is_guest(self):
        """Checking for unauthorized user rights (guest)."""
        return self.role == self.GUEST

    @property
    def is_authorized(self):
        """Checking for authorized user rights."""
        return self.role == self.AUTHORIZED

    @property
    def is_admin(self):
        """Checking for administrator rights."""
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        # constraints = [
        #     models.CheckConstraint(
        #         check=~models.Q(username__iexact="me"),
        #         name="username_is_not_me"
        #     )
        # ]
    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Подписка на автора рецепта."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор рецепта',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} subscribed on {self.author}'
