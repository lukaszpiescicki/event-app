from rest_framework.viewsets import ModelViewSet

from users.models import CustomUser

from .serializers import UserSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
