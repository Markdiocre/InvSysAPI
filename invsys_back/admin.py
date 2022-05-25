from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Categories, UserGroup
from .forms import UserCreationform, UserChangeForm

admin.site.site_header = 'Inventory System'
admin.site.site_title = 'Inventory System Admin Panel'
admin.site.index_title = 'Welcome to Inventory System Admin'


# Register your models here.

class UserAdmin(BaseUserAdmin):

    ordering = ['-username']
    list_display=[
        'user_id','username','name','user_level','is_active','is_staff','last_login'
    ]
    list_filter = ['is_staff','is_active']
    search_fields=[
        'username','name',
    ]
    fieldsets=[
        [None,{'fields':['username','name','user_level','password','last_login']}],
        ['Permissions', {'fields':['is_active','is_staff']}],
    ]
    add_fieldsets = [
        [None,{
            'classes':['wide',],
            'fields':['username','name','user_level','last_login','password1','password2','is_staff','is_active']
        }]
    ] 

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id','name']
    search_fields=['name',]

class UserGroupsAdmin(admin.ModelAdmin):
    list_display = ['user_group_id','group_name','group_level','group_status']

admin.site.register(User, UserAdmin)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(UserGroup, UserGroupsAdmin)
admin.site.unregister(Group)
