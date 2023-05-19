from django.contrib import admin
from book_model.models import Book


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'pub_date', 'availability', 'price',)
    list_filter = ('genre', 'pub_date')
    search_fields = ('title', 'genre')
    actions_on_top = False
    list_per_page = 20


admin.site.register(Book, BookAdmin)
