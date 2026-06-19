from django.contrib import admin

from .models import Cart, CartItem, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock", "category", "created_at")
    search_fields = ("name", "category")
    list_filter = ("category", "created_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "status", "payment_method", "order_date")
    list_filter = ("status", "payment_method", "order_date")
    search_fields = ("user__email", "id")



admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)

