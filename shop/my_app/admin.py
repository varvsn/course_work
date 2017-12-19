from django.contrib import admin
from .models import Shop_Item, UsersAndOrders, Orders


class AllOrdersInline(admin.TabularInline):
    model = Orders


class OrdersAll(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'comment', 'total_sum',)
    search_fields = ('id', 'order_date')
    ordering = ['id']
#    readonly_fields = ('total_sum',)
    inlines = [
        AllOrdersInline,
    ]

class ShopItemExtend(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'created_date')
    search_fields = ('id', 'name', 'description', 'foreign_key__order')
    list_display_links = ('id', 'name')
    ordering = ['id', 'name']



admin.site.register(Shop_Item, ShopItemExtend)
admin.site.register(UsersAndOrders, OrdersAll)
#admin.site.register(Orders)

