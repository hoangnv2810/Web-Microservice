from django.contrib import admin
from cart.models import Cart, CartItem


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_item', 'total_price', 'created_at',)
    list_filter = ('user', 'created_at',)
    search_fields = ('user',)
    actions_on_top = False
    list_per_page = 20


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity',)
    search_fields = ('product',)
    list_filter = ('cart', )
    actions_on_top = False
    list_per_page = 20


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
