
from rest_framework import viewsets

from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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
    queryset = Batch.objects.all().order_by('-quantity')
    permission_classes = [IsAuthenticated,]
    serializer_class = BatchSerializer

class RequesitionView(viewsets.ModelViewSet):
    queryset = Requesition.objects.all().order_by('request_date')
    permission_classes = [IsAuthenticated,]
    serializer_class = RequesitionSerializer

class DashboardView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request,format=None):
        total_products = Product.objects.all().count()
        low_stock_products = []
        for prod in Product.objects.all():
            if prod.total_quantity() < prod.reordering_point and prod.total_quantity() > 0:
                low_stock_products.append(prod)

        out_of_stock = []
        for prod in Product.objects.all():
            if prod.total_quantity() == 0:
                out_of_stock.append(prod)
        
        most_stock_product = []
        for prod in Product.objects.all():
            if prod.total_quantity() >= 50:
                most_stock_product.append(prod)

        return Response({
            "total": total_products,
            "low_stock_count": len(low_stock_products),
            "out_of_stock_count": len(out_of_stock),
            "most_stock_product_count": len(most_stock_product),
        })

class RecentFiveRequestView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        requesition = Requesition.objects.all().order_by('request_date')[:15]
        serializer = RequesitionSerializer(requesition, many=True)
        return Response(serializer.data)

class RecentFiveBatchView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        batches = Batch.objects.all().order_by('date_added')[:15]
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data)

class RecentFiveProductView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        products = Product.objects.all().order_by('date_created')[:15]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
