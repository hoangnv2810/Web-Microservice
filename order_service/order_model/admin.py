from django.contrib import admin

from .models import Order, OrderItem


# Register your models here.
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order',)
    list_per_page = 20


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'number_phone', 'total_price', 'created_at', 'is_paid')
    search_fields = ('username', 'number_phone',)
    list_filter = ('created_at', 'is_paid',)
    list_per_page = 20
    list_display_links = ('username',)
    actions_selection_counter = False


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)