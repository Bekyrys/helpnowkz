from django.contrib import admin

# Register your models here.
from .models import *
from .models import ShippingAddreess

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order', 'address', 'tel_number', 'comment', 'date_added']
    readonly_fields = ['display_order_items']
    search_fields = ['customer__name', 'address', 'tel_number'] # Добавляет поля для поиска
    list_filter = ['customer', 'order', 'date_added', 'tel_number'] # Добавляет поля для фильтрации
    # display_order_items.short_description = 'Заказанные товары' # Название для отображаемого поля

    
    def display_order_items(self, obj):
        order_items = obj.order.orderitem_set.all()
        return ', '.join([f"{item.product.name} (x{item.quantity})" for item in order_items])

# class ShippingAddressAdmin(admin.ModelAdmin):
#     list_display = ['customer', 'order', 'address', 'tel_number', 'comment', 'date_added']

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(ShippingAddreess)
admin.site.register(ShippingAddreess, ShippingAddressAdmin)


# admin.site.register(ShippingAddreess, ShippingAddressAdmin)