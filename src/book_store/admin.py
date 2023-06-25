from django.contrib import admin
from .models import Book, Order, Customer, CartItem

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'ex_price', 'price', 'publication_date')
    search_fields = ('price', 'title')
    list_filter = ('price', 'author')
    list_editable = ('price',)
    date_hierarchy = 'created_at'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'customer', 'quantity', 'price', 'status')
    search_fields = ( 'book__title',)
    list_filter = ('price', 'status', 'quantity')
    list_editable = ('status',)
    date_hierarchy = 'created_at'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone')
    search_fields = ('email', 'phone')

admin.site.register(CartItem)