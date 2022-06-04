
from nis import match
from rest_framework import viewsets

from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import  CategorySerializer, InventorySerializer, MonthlyReportSerializer, ProductSerializer, RequesitionSerializer, UserGroupSerializer
from .models import Categories, Inventory, Product, Requesition, UserGroup
from .permissions import AdminLevelOnlyPermission
from .paginations import StandardResultsSetPagination

import datetime


# Create your views here.
class CategoryView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

class UserGroupView(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    permission_classes = [IsAuthenticated, AdminLevelOnlyPermission,]
    serializer_class = UserGroupSerializer
    pagination_class = StandardResultsSetPagination

class LoginToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=result.data['token'])
        update_last_login(None, token.user)
        return result

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('date_created')
    permission_classes = [IsAuthenticated,
    ]
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

class InventoryView(viewsets.ModelViewSet):
    queryset = Inventory.objects.all().order_by('-quantity')
    permission_classes = [IsAuthenticated,]
    serializer_class = InventorySerializer
    pagination_class = StandardResultsSetPagination

class RequesitionView(viewsets.ModelViewSet):
    queryset = Requesition.objects.all().order_by('request_date')
    permission_classes = [IsAuthenticated,]
    serializer_class = RequesitionSerializer
    pagination_class = StandardResultsSetPagination

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

class RecentRequestView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        requesition = Requesition.objects.all().order_by('request_date')[:15]
        serializer = RequesitionSerializer(requesition, many=True)
        return Response(serializer.data)

class RecentInventoryView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        inventories = Inventory.objects.all().order_by('date_added')[:15]
        serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data)

class RecentProductView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        products = Product.objects.all().order_by('date_created')[:15]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class GetAllProductView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class GetAllInventoryView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        inventories = Inventory.objects.all()
        serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data)

class GetAllCategoryView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        categories = Categories.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
        
class GetAllUserGroupView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        user_groups = UserGroup.objects.all()
        serializer = UserGroupSerializer(user_groups, many=True)
        return Response(serializer.data)

class MonthReportView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, format=None):
        
        report = {
            'products' : [],
            'grand_total' : 0
        }

        for product in Product.objects.all():
            grand_total = 0
            total = 0
            for req in Requesition.objects.all().filter(remarks='a', request_date__month = request.data['month'], request_date__year = request.data['year']):
                total = total + req.quantity
            
            products = ProductSerializer(product).data
            products['monthly_total']  = total
            products['monthly_total_cost'] = total * product.selling_price
            
            report['products'].append(products)
            grand_total = grand_total + total
            
        report['grand_total'] = grand_total

        return Response(report)

class YearlyReportView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, format=None):
        
        report = {
            'products' : [],
            'grand_total' : 0
        }

        for product in Product.objects.all():
            grand_total = 0
            total = 0
            for req in Requesition.objects.all().filter(remarks='a', request_date__year = request.data['year']):
                total = total + req.quantity
            
            products = ProductSerializer(product).data
            products['yearly_total']  = total
            products['yearly_total_cost'] = total * product.selling_price
            grand_total = grand_total + total
            report['products'].append(products)

        report['grand_total'] = grand_total

        return Response(report)

class QuarterlyReportView(APIView):
    permission_classes = [IsAuthenticated,]

    quarters = {
        '1':{
            'start_day' : 1,
            'start_month' : 1,
            'end_day' : 31,
            'end_month' : 3
        },
        '2':{
            'start_day' : 1,
            'start_month' : 4,
            'end_day' : 30,
            'end_month' : 6,
        },
        '3':{
            'start_day' : 1,
            'start_month' : 7,
            'end_day' : 30,
            'end_month' : 9,
        },
        '4':{
            'start_day' : 1,
            'start_month' : 10,
            'end_day' : 31,
            'end_month' : 12
        }
    }

    def post(self, request, format=None):
        report = {
            'products' : [],
            'grand_total' : 0
        }


        start_date = datetime.date(request.data['year'], self.quarters[request.data['quarter']]['start_month'], self.quarters[request.data['quarter']]['start_day'])
        end_date = datetime.date(request.data['year'], self.quarters[request.data['quarter']]['end_month'], self.quarters[request.data['quarter']]['end_day'])
        
        for product in Product.objects.all():
            grand_total = 0
            total = 0
            for req in Requesition.objects.all().filter(remarks='a', request_date__range = (start_date,end_date)):
                total = total + req.quantity
            
            products = ProductSerializer(product).data
            products['quarterly_total']  = total
            products['quarterly_total_cost'] = total * product.selling_price
            grand_total = grand_total + total
            report['products'].append(products)

        report['grand_total'] = grand_total

        return Response(report)
