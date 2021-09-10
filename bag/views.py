from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product

# Create your views here.


def view_bag(request):  # request is a method
    # Aview that rendes the bag contents page

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ add a quantity of the specified product to the shopping bag """
    print(request.POST)  # look at the format below:
    # ... QueryDict: {'csrfmiddlewaretoken': ['ZactJe12aSMSuYrwnj5uKNwh55OKYGfH5gSIXxsvZo8vr1AUuanMKMRmbyt4cchh'], 'product_size': ['m'], 'quantity': ['2'], 'redirect_url': ['/products/122']}
    product = get_object_or_404(Product, pk=item_id)
    print(type(type(request.POST.get('quantity'))))
    # request.POST.get('quantity') is a string like number string
    quantity = int(request.POST.get('quantity'))  # needs to have int because
    # ... comes as template from request
    redirect_url = request.POST.get('redirect_url')
    print(redirect_url + ' = redirect_url ---------***********-----------------**************------------')
    # redirect_url format '/products/122'
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
        print(size + ' = size ---------***********-----------------**************------------')

    # creating a session. It stores in the HTTP until the user closes the browser
    print(request.session)
    # format of request.session {'56': {'items_by_size': {'m': 1}}, '11': {'items_by_size': {'m': 1, 'l': 1}}, '21': 1, '22': 1, '122': {'items_by_size': {'m': 24}}}
    print('above print reques.session---------***********-----------------**************------------')
    bag = request.session.get('bag', {})  # initialized with empty dictionary
    print(bag)
    print('above is the bag = request.session.get("bag", ) ---------***********-----------------**************------------')

# if size is added to the item going to the card, handle things differently
# it will be rendered in dictionary format because we can have one item but multiple sizes
    if size:
        # if item is already in the bag
        if item_id in list(bag.keys()):
            print(list(bag.keys()))
            # format of baf.keys() ['56', '11', '21', '22', '122', '49', '121']
            print(' above is the list(bag.keys()) ---------***********-----------------**************------------')
            # if item with same id and same size increment the item
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')

            else:
                # add the item and quantity
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} { product.name} to your bag')

        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} { product.name} to your bag')
    else:
        # if there is a bag.keys add quantity, if not create bag_id
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Added {product.name} quantity to your bag {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')


    # put the bag variable inside of the session which is a dictionary. This bag has all items inside the bag currently
    request.session['bag'] = bag
    print(request.session['bag'])
    print('above is request session ---------***********-----------------**************------------')
    # {'1': {'items_by_size': {'m': 2}}, '122': {'items_by_size': {'m': 9, 'l': 8, 'xs': 1}}}
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    print('is adjust_bag running at all? ---------***********-----------------**************------------')
    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            print(bag[item_id]['items_by_size'][size])
            print('above is bag[item_id][items_by_size][size] ---------***********-----------------**************------------')
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')

        else:
            del bag[item_id]['items_by_size'][size]  # delete the specific size
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)  # delete item of all sizes
                messages.success(request, f'Removed size {size.upper()} { product.name} from your bag')

    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} quantity to your bag {bag[item_id]}')

        else:
            bag.pop(item_id)
            messages.success(request, f'Remove {product.name} from your bag')


    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    print('is adjust_bag running at all? ---------***********-----------------**************------------')

    try:
        product = get_object_or_404(Product, pk=item_id)

        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} { product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Remove {product.name} from your bag')


        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
