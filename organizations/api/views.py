from rest_framework.viewsets import ModelViewSet

from organizations.models import Organization

from .serializers import OrganizationSerializer


class OrganizationModelViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
