from django.contrib import admin
from .models import Shop_Item, UsersAndOrders, Orders

admin.site.register(Shop_Item)
admin.site.register(UsersAndOrders)
admin.site.register(Orders)

