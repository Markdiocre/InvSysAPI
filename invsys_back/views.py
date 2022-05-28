
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from djoser.views import UserViewSet as UVS
from djoser.conf import settings


from .serializers import CategorySerializer, UserGroupSerializer, UserSerializer
from .models import Categories, UserGroup
from .permissions import AdminLevelOnlyPermission, CurrentUserOrAdminLevel


# Create your views here.
class CategoryView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = CategorySerializer

class UserGroupView(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    permission_classes = [IsAuthenticated, AdminLevelOnlyPermission,]
    serializer_class = UserGroupSerializer

class LoginToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=result.data['token'])
        update_last_login(None, token.user)
        return result

