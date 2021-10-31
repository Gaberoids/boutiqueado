from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from bag.contexts import bag_contents  # to access the total_cost
from .forms import OrderForm

import stripe


# Create your views here.
def checkout(request):
    # stripe
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        # below will prevent someone from going to checkout by typing /checkout
        return redirect(reverse('products'))
    #getting the total from bag_contents
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

    print(" Payment intent : ---------***********-----------------**************------------")
    print(intent)
    # intent is like a dictionary with a bunch of keys

    # create instance of order form
    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
