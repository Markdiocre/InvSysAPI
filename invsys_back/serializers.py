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
        fields = ['product_id','category','name','measuring_name','reordering_point','selling_price','total_quantity','remarks',]
        read_only_fields = ['total_quantity','remarks',]


class BatchSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Batch
        fields = '__all__'

class RequesitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requesition
        fields = '__all__'

    def create(self, validated_data):
        batch_id = validated_data.get('batch').batch_id
        batch = Batch.objects.get(batch_id= batch_id)

        #Checks if the batch quantity will be below zero
        if (batch.quantity - validated_data.get('quantity') < 0 ):
            raise serializers.ValidationError("Batch quantity must not be below 0 after request")
        else:

            #Reduce that batch quantity then create the request
            batch.quantity = batch.quantity - validated_data.get('quantity')
            batch.save()
            return Requesition.objects.create(**validated_data)



class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username','name', 'user_level','password', 'last_login','is_active')

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('user_id','username','name', 'user_level', 'last_login','is_active')
        read_only_fields= None

    
