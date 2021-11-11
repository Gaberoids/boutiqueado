from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
# product.models. product is the application name
from products.models import Product
from bag.contexts import bag_contents  # to access the total_cost

import stripe
import json


# below block is to make sure everything goes to the database
# even though the user may close the window before the transaction is over
@require_POST
def cache_checkout_data(request):
    print("checkout/views.py cache_checkout_data function is running---------***********-----------------**************------------")
    try:
        print("checkout/views.py cache_checkout_data>TRY function is running---------***********-----------------**************------------")
        # pit = payment intent id
        pid = request.POST.get('client_secret').split('_secret')[0]
        # set up stripe with secret key so we can modify pay intent/next 2 lines
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            # below bag is to be used later
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        print("checkout/views.py cache_checkout_data TRY END---------***********-----------------**************------------")
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


# Create your views here.
def checkout(request):
    print('INSIDE CHECKOUT ---------***********-----------------**************------------')
    # stripe
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        print("POST RUNNING IF POST >>>>>>>>>>>>>")
        # create an instance of the form using the form data
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        # if the form is valid, save and iterate
        # if not order_form.is_valid():
        #     print("FORM IS NOT VALID")
        #     print(order_form.errors)
        if order_form.is_valid():
            print('INSIDE IS_VALID IF  ---------***********-----------------**************------------')
            order = order_form.save(commit=False)
            # commit=false will prevent multipe savings. First save wont happen

            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                print('INSIDE is_valid/FOR ---------***********-----------------**************------------')
                try:
                    print('checkout/views.py INSIDE formisvalid/TRY  ---------***********-----------------**************------------')
                    # below: get product id from the bag
                    product = Product.objects.get(id=item_id)
                    print("checkout/views.py product is below---------***********-----------------**************------------")
                    print(product)
                    print("final, product value---------***********-----------------**************------------")
                    # if interger we know that there is no size
                    if isinstance(item_data, int):
                        print('IF IS INSTANCE ---------***********-----------------**************------------')
                        print(order)
                        print(product)
                        print(item_data)
                        print("end of order, product, item_data ---------***********-----------------**************------------")
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                            # no product_size
                        )
                        print("before sabe order line item---------***********-----------------**************------------")
                        order_line_item.save()
                        print("after orderline item.save ---------***********-----------------**************------------")
                    else:
                        print('ELSE INSIDE ISINSTANCE ---------***********-----------------**************------------')
                        # with size create a line_order accordingly
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                # it should not happen but if a product does not exist...
                except Product.DoesNotExist:
                    print('checkout/views.py EXCEPT IF Product.DoesNotExist ---------***********-----------------**************------------')
                    messages.error(request, (
                        "One of the products in your bag wasn't "
                        "found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))
    else:
        print("GET RUNNING >>>>>>>>>>>>>>>>>>>>>>>>>>")
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            # below will prevent someone from going to checkout by typing /checkout
            return redirect(reverse('products'))
        # getting the total from bag_contents
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        # stripe require an interger therefore next line
        stripe_total = round(total * 100)
        # set the  secret key on stripe
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # print(" Payment intent : ---------***********-----------------**************------------")
        # print(intent)
        # Aboveintent is like a dictionary with a bunch of keys
        # create instance of order form
        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, ('Stripe public key is missing. \
            Did you forget to set it in your environment?'))

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    necessary when we create user profiles
    """
    print("checkout/Views.py save_info is below ---------***********-----------------**************------------")
    save_info = request.session.get('save_info')
    print(save_info)
    print("checkout/Views.py save_info end ---------***********-----------------**************------------")

    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # since at theis point you wont need the session bag, you can deleted
    if 'bag' in request.session:
        print("checkout/views.py inside IF Bag ---------***********-----------------**************------------")
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    print("checkout/view.py return is below---------***********-----------------**************------------")
    return render(request, template, context)
