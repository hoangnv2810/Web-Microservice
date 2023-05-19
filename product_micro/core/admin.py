from django.contrib import admin

from core.models import Category, Product


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    search_fields = ('category_name',)
    list_per_page = 20


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'stock', 'category', 'modified_date',)
    list_filter = ('category', 'modified_date')
    search_fields = ('product_name', 'category')
    actions_on_top = False
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
