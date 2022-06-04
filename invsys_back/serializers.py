from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer, UserSerializer as BaseUserSerializer
from .models import Inventory, Categories, Product, Requesition, UserGroup
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category_id','name']

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['user_group_id','group_name','group_level','group_status']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id','category','get_category_name','name','measuring_name','date_created','reordering_point','selling_price','total_quantity','remarks',]
        read_only_fields = ['total_quantity','remarks','get_category_name']


class InventorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Inventory
        fields = ['inventory_id','user','product','quantity','date_purchased','expiration_date','get_product_name','get_user_name','get_user_department','get_category_name']
        read_only_fields = ['get_product_name','get_user_name','get_user_department','get_category_name']

class RequesitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requesition
        fields = ['request_id','user', 'inventory', 'product', 'quantity','request_date','remarks','get_user_name','get_user_department','get_inventory_name','get_product_name','get_remarks']
        read_only_fields = ['get_user_name','get_user_department','get_inventory_name','get_product_name','get_remarks']

    def update(self, instance, validated_data):
        if(validated_data.get('remarks') == 'a' ):
            inventory_id = instance.inventory.inventory_id
            inventory = Inventory.objects.get(inventory_id=inventory_id)

            #Checks if the inventory quantity will be below zero
            if (inventory.quantity - instance.quantity < 0 ):
                raise serializers.ValidationError("Inventory quantity must not be below 0 after approval")
            else:

                #Reduce that inventory quantity then create the request
                inventory.quantity = inventory.quantity - instance.quantity
                inventory.save()
        else:
            inventory_id = instance.inventory.inventory_id
            inventory = Inventory.objects.get(inventory_id = inventory_id)
            inventory.quantity = inventory.quantity + instance.quantity
            inventory.save()

        instance.remarks = validated_data.get('remarks')
        instance.save()
        return instance



class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username','name', 'user_level','password', 'last_login','is_active')

class UserSerializer(BaseUserSerializer):
    user_level_equivalent = serializers.IntegerField(source='get_user_level')
    user_group_name = serializers.CharField(source='get_user_group_name')

    class Meta(BaseUserSerializer.Meta):
        fields = ['user_id','username','name', 'user_level', 'last_login','is_active','user_level_equivalent','user_group_name']
        read_only_fields= ['user_level_equivalent','user_group_name']

class MonthlyReportSerializer(serializers.BaseSerializer):
    product = ProductSerializer()
    total = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'product': instance.product,
            'total': instance.total
        }

    class Meta:
        fields = ['product','total']
        read_only_fields = ['product','total']
