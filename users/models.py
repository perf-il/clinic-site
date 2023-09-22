from django.db import models
from django.contrib.auth.models import AbstractUser


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='E-mail', unique=True)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Подтверждение e-mail')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
