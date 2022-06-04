from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


# Create your models here.
class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserGroup(models.Model):
    user_group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=255)
    group_level = models.IntegerField()
    group_status = models.BooleanField(default=True)

    def __str__(self):
        return self.group_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    measuring_name = models.CharField(max_length=10)
    reordering_point = models.PositiveIntegerField()
    selling_price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name

    def total_quantity(self):
        inventories = Inventory.objects.filter(product=self.product_id)
        total = 0
        for inventory in inventories:
            total = total + inventory.quantity
        return total

    def get_category_name(self):
        return self.category.name

    def remarks(self):
        msg = 'OK'
        if self.total_quantity() < self.reordering_point:
            msg = 'For Replenish'
            return msg
        return msg


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # reference_no = models.AutoField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_purchased = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.inventory_id,self.quantity)

    def get_product_name(self):
        return self.product.name

    def get_user_name(self):
        return self.user.name

    def get_user_department(self):
        return self.user.user_level.group_name

    def get_category_name(self):
        return self.product.category.name


class Requesition(models.Model):
    remarks = [
        ('a','Accepted'),
        ('r', 'Rejected'),
        ('p', 'Pending'),
    ]

    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    request_date = models.DateTimeField(auto_now=True)
    remarks = models.CharField(choices=remarks, default='p', max_length=2)

    def __str__(self):
        return '{} - {}'.format(self.user,self.product)

    def get_user_name(self):
        return self.user.name

    def get_user_department(self):
        return self.user.user_level.group_name

    def get_inventory_name(self):
        return self.inventory.inventory_id

    def get_product_name(self):
        return self.product.name
        
    def get_remarks(self):
    	return self.get_remarks_display()

# CUSTOM USER CLASS
class CustomUserManager(BaseUserManager):
    def create_user(self, username ,password, **other_fields):
        other_fields.setdefault('is_active', True)  
        user = self.model(username=username,**other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username,password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assined to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assined to is_superuser=True')


        return self.create_user(username, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    user_level = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null= True,blank=True)
    last_login = models.DateTimeField(blank=True, null=True)

    #Administration Rights (A MUST)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['name',]
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_user_id(self):
        return self.user_id

    def get_user_level(self):
        return self.user_level.group_level

    def get_user_group_name(self):
        return self.user_level.group_name


