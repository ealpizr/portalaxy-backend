"""Portfolios serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from api.groups.serializers import GroupModelSerializer

# Models
from api.portfolios.models import Portfolio

class PortfolioModelSerializer(serializers.ModelSerializer):
    """Portfolio model serializer."""

    group = GroupModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = Portfolio

        fields = [
            'group'
        ]

        read_only_fields = [
            'group'
        ]