"""Group views."""

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Serializer
from api.groups.serializers import GroupModelSerializer
from api.portfolios.serializers import PortfolioModelSerializer

# Models
from api.groups.models import Group, Membership
from api.portfolios.models import Portfolio

# Permissions
from api.groups.permissions import IsGroupAdmin

class GroupViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Group view set."""
    serializer_class = GroupModelSerializer

    def get_queryset(self):
        """Restrict list to public-only groups."""
        queryset = Group.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        #if self.action == 'retrieve':
            #return Portfolio.objects.all()
        return queryset

    def retrieve(self, request, pk=None):
        print(pk)
        return Response(PortfolioModelSerializer(Portfolio.objects.filter(group=Group.objects.get(slug_name=pk))).data)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsGroupAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Assign group admin."""
        group = serializer.save()
        user = self.request.user
        Membership.objects.create(
            user=user,
            group=group,
            is_admin=True
        )