from django.contrib import admin
from store.models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 24


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'availibility', 'updated', 'created')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)
    list_editable = ('price', 'availibility')
    list_per_page = 24

from .models import Contact
admin.site.register(Contact)
