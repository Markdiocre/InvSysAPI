
from rest_framework import viewsets

from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.response import Response


from .serializers import BatchSerializer, CategorySerializer, ProductSerializer, RequesitionSerializer, UserGroupSerializer
from .models import Batch, Categories, Product, Requesition, UserGroup
from .permissions import AdminLevelOnlyPermission


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

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated,
    ]
    serializer_class = ProductSerializer

class BatchView(viewsets.ModelViewSet):
    queryset = Batch.objects.exclude(quantity=0).order_by('date_added')
    permission_classes = [IsAuthenticated,]
    serializer_class = BatchSerializer

class RequesitionView(viewsets.ModelViewSet):
    queryset = Requesition.objects.all().order_by('request_date')
    permission_classes = [IsAuthenticated,]
    serializer_class = RequesitionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        batch = Batch.objects.get(batch_id = instance.batch.batch_id)
        batch.quantity = batch.quantity + instance.quantity
        batch.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)