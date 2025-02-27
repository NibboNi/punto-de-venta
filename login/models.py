from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPES = (
        ("admin", "Administrador"),
        ("venta", "Vendedor"),
    )

    role = models.CharField(
        max_length=20, choices=USER_TYPES, default='venta')

    def __str__(self):
        return self.username
