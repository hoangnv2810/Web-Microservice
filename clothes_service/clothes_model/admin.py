from django.contrib import admin

from clothes_model.models import Clothes


# Register your models her
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'size', 'categories', 'availability', 'price',)
    list_filter = ('categories', 'brand')
    search_fields = ('title', 'genre')
    actions_on_top = False
    list_per_page = 20


admin.site.register(Clothes, ClothesAdmin)