from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer, UserSerializer as BaseUserSerializer
from .models import Batch, Categories, Product, Requesition, UserGroup
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
        fields = ['product_id','category','name','measuring_name','date_created','reordering_point','selling_price','total_quantity','remarks',]
        read_only_fields = ['total_quantity','remarks',]


class BatchSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Batch
        fields = ['batch_id','user','batch_name','product','quantity','date_added','expiration_date','get_product_name','get_user_name','get_user_department']
        read_only_fields = ['get_product_name','get_user_name','get_user_department']

class RequesitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requesition
        fields = ['request_id','user', 'batch', 'product', 'quantity','request_date','is_approved','get_user_name','get_user_department','get_batch_name','get_product_name']
        read_only_fields = ['get_user_name','get_user_department','get_batch_name','get_product_name']

    def update(self, instance, validated_data):
        if(validated_data.get('is_approved') == True ):
            batch_id = instance.batch.batch_id
            print(batch_id)
            batch = Batch.objects.get(batch_id=batch_id)

            #Checks if the batch quantity will be below zero
            if (batch.quantity - instance.quantity < 0 ):
                raise serializers.ValidationError("Batch quantity must not be below 0 after approval")
            else:

                #Reduce that batch quantity then create the request
                batch.quantity = batch.quantity - instance.quantity
                batch.save()
        else:
            batch_id = instance.batch.batch_id
            batch = Batch.objects.get(batch_id = batch_id)
            batch.quantity = batch.quantity + instance.quantity
            batch.save()

        instance.is_approved = validated_data.get('is_approved')
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

    
