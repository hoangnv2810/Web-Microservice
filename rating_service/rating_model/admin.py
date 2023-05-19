from django.contrib import admin
from .models import Rating


# Register your models here.
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'order_id', 'category', 'product_id', 'rating', 'comment', 'created_at')


admin.site.register(Rating, RatingAdmin)
