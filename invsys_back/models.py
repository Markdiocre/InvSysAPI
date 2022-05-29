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

    def __str__(self):
        return self.name

    def total_quantity(self):
        batches = Batch.objects.filter(product=self.product_id)
        total = 0
        for batch in batches:
            total = total + batch.quantity
        return total

    def remarks(self):
        msg = 'OK'
        if self.total_quantity() < self.reordering_point:
            msg = 'For Replenish'
            return msg
        return msg


class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=20, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.batch_name,self.quantity)


class Requesition(models.Model):
    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    request_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.user,self.product)

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


