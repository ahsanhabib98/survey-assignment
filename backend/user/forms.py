from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import (
    User
)


class AdminSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        if commit:
            user.save()
        return user