from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'null': True, 'blank': True}
class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(verbose_name='Аватар', **NULLABLE, upload_to='user/avatars')
    telephone = models.CharField(verbose_name='Номер телефона', **NULLABLE)
    tg_chat_id = models.CharField(
        max_length=50, verbose_name="Телеграм chat-id", **NULLABLE
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'