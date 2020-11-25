"""Group models."""

# Django
from django.db import models


class Group(models.Model):
    """Group model."""
    name = models.CharField(
        max_length=50
    )

    slug_name = models.SlugField(
        unique=True
    )

    picture = models.ImageField(blank=True, null=True)

    is_public = models.BooleanField()

    is_verified = models.BooleanField()

    members = models.ManyToManyField(
        'users.User',
        through='groups.Membership',
        through_fields=('group', 'user')
    )