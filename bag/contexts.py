from decimal import Decimal  # when working with money values is
# ...better to use decimals than 'flow'
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


#  the purpose is to make available variable to all templates accross
# ...the website
def bag_contents(request):
    print(request)
    print('ABOVE is a ,request, value from bag_content function found in the context.py. this is meant to tell me when this this context and function runs ---------***********-----------------**************------------')
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

# item_data is equal quantity if no has_size
# ... if has_size true item_data  is equal to a list dictionary of all items by size 
    for item_id, item_data in bag.items():
        if isinstance(item_data, int):  # integer mean has_size false, item_data is quantity which is integer
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:  # settings =  boutique_ado >
        # ...settings.py
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
