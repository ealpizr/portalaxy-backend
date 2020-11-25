"""Membership model."""

# Django
from django.db import models


class Membership(models.Model):
    """
    Membership model.

    A membership is a table that holds the relationship
    between a user and a group.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        'group admin',
        default=False,
        help_text="Group admins can update the group's data and manage its members."
    )