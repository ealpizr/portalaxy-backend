"""Group serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from api.groups.models.groups import Group


class GroupModelSerializer(serializers.ModelSerializer):
    """Group model serializer."""

    is_public = serializers.BooleanField(default=True)
    is_verified = serializers.BooleanField(default=False)
    picture = serializers.ImageField(required=False)

    class Meta:
        """Meta class."""
        model = Group
        fields = [
            'name',
            'slug_name',
            'picture',
            'is_public',
            'is_verified'
        ]
        read_only_fields = [
            'is_verified'
        ]