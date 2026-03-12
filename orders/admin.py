from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('food', 'quantity', 'price', 'total_price')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'id')
    readonly_fields = ('user', 'total_amount', 'created_at')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'user', 'total_amount', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'food', 'quantity', 'price', 'total_price')
    list_filter = ('order__created_at', 'food')
    search_fields = ('order__id', 'food__name')
    readonly_fields = ('total_price',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'food', 'quantity', 'total_price')
    search_fields = ('cart__user__username', 'food__name')
    readonly_fields = ('total_price',)
