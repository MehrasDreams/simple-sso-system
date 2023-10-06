from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse

from .manager import UserManager


class Profile(AbstractBaseUser):
    phone = models.CharField(unique=True, max_length=12)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=True, null=True)


    objects = UserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UsersToken(models.Model):
    token = models.TextField()
    user = models.IntegerField()

    def __str__(self):
        return str(f'Token for user {self.user}')

