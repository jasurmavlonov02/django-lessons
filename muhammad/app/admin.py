from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import Product, Category, User


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'price', 'amount']
    fields = ['title', 'price','category', 'description','amount']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug','product_count']
    fields = ['image', 'name']
    search_fields = ['name']

    def product_count(self,obj):
        return obj.product_set.count()


admin.site.register(User,UserAdmin)
