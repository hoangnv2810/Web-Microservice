from django.contrib import admin

from cart_model.models import cart, cart_item


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'total_price', 'created_at')


admin.site.register(cart, CartAdmin)
admin.site.register(cart_item)
