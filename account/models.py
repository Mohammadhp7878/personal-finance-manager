from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(regex=r"^\d{11}", message="شماره تلفن نامعتبر است.")
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
