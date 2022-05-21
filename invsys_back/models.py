from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
    user_level = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null= True)
    last_login = models.DateTimeField()

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


