from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
