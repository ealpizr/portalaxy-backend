"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

# Managers
from api.users.managers.users import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model.

    Extend from Django's Abstract Base User, change the username field
    to email and add some extra fields.
    """
    email = models.EmailField(
        'email adress',
        unique=True,
        error_messages={
            'unique': 'A user with that email adress already exists.'
        }
    )

    first_name = models.CharField(
        'first name',
        max_length=30
    )

    last_name = models.CharField(
        'last name',
        max_length=30
    )

    picture = models.ImageField(
        'profile picture',
        upload_to = 'users/pictures/',
        blank=True,
        null=True
    )

    date_joined = models.DateTimeField(
        'date joined',
        auto_now_add=True
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user has verified its email address.'
    )

    is_staff = models.BooleanField(
        'staff',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    objects = UserManager()

    def __str__(self):
        """Return user's email"""
        return self.email