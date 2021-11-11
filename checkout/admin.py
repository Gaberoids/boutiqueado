from django.contrib import admin
from .models import Order, OrderLineItem


# class to allow to pass and add items in line instead of going to
# ... edit item interface
class OrderLineItemAdminInLine(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

# Register your models here. Edit item interface
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInLine,)

    # fields that will be calculated by models
    readonly_fields = ('order_number', 'date', 
                       'delivery_cost', 'order_total', 
                       'grand_total', 'original_bag', 'stripe_pid')

    # this is to allow ordering of fields. 
    # ... Read only fields are orderd by django
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag', 'stripe_pid')

    # to restric the display of fields to only key items
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost', 'grand_total')

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)