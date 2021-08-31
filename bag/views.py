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
    # creating a session. It stores in the HTTP until the user closes the browser
    bag = request.session.get('bag', {})  # initialized with empty dictionary

# if there is a bag.keys add quantity, if not create bag_id
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # put the bag variable inside of the session which is a dictionary
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)