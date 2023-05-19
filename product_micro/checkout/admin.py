from django.contrib import admin

from checkout.models import Order, OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order',)
    list_per_page = 20


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'number_phone', 'total_price', 'created_at', 'is_delivered', 'is_paid')
    search_fields = ('user', 'number_phone',)
    list_filter = ('created_at', 'is_paid', 'is_delivered',)
    list_per_page = 20
    readonly_fields = ('user',)
    list_display_links = ('user',)
    actions_selection_counter = False


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
