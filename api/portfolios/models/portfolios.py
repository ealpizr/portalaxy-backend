"""Portfolios models."""

# Django
from django.db import models

class Portfolio(models.Model):
    """Portfolio model."""

    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)

    name = models.CharField(max_length=30)