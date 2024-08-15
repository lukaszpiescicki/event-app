from organizations.models import Organization
from rest_framework.viewsets import ModelViewSet

from .serializers import OrganizationSerializer


class OrganizationModelViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
