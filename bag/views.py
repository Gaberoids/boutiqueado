from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):  # request is a method
    # Aview that rendes the bag contents page

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))  # needs to have int because
    # ... comes as template from request
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    # creating a session. It stores in the HTTP until the user closes the browser
    bag = request.session.get('bag', {})  # initialized with empty dictionary

# if size is added to the item going to the card, handle things differently
# it will be rendered in dictionary format because we can have one item but multiple sizes
    if size:
        # if item is already in the bag
        if item_id in list(bag.keys()):
            # if item with same id and same size increment the item
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # add the item and quantity
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # if there is a bag.keys add quantity, if not create bag_id
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity


    # put the bag variable inside of the session which is a dictionary
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)