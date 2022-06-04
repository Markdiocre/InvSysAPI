from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Categories, UserGroup, Inventory, Product, Requesition
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

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['inventory_id', 'product','user', 'quantity','expiration_date','date_purchased']
    search_fields=['inventory_id','product','user']

class ProductAdmin(admin.ModelAdmin):
    list_display=['product_id','category','name','measuring_name','reordering_point','selling_price','total_quantity','remarks',]
    search_fields=['name',]
    list_filter = ['category',]

class RequesitionAdmin(admin.ModelAdmin):
    list_display=['request_id','user','product','quantity','request_date']

admin.site.register(User, UserAdmin)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(UserGroup, UserGroupsAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Requesition, RequesitionAdmin)
admin.site.unregister(Group)
