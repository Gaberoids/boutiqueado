from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""
    # init runs every time a instance of this class is created
    def __init__(self, request):
        self.request = request
        print("Create 'request' from webhook_handler>StripeWH_handler> __init__ \
            ---------***********-----------------\
                **************------------")
        print(request)
        print("from webhook_handler>StripeWH_handler Print self: ---------***********-----------------**************------------")
        print(self)

    def handle_event(self, event):
        """
        Handle a generic/unknown/nuexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        # below block is to make sure everything goes to the database
        # even though the user may close the window before the transaction is over
        # combined with views.py>cache view
        intent = event.data.object
        print(" intent value below ---------***********-----------------**************------------")
        print(intent)
        print(" intent value end ---------***********-----------------**************------------")

        pid = intent.id
        print("wbh_handler.py pid is above---------***********-----------------**************------------")
        print("wbh_handler.py bag below ---------***********-----------------**************------------")
        print(intent.metadata.bag)
        bag = intent.metadata.bag
        print("wbh_handler.py bag is above ---------***********-----------------**************------------")
        save_info = intent.metadata.save_info
        print(save_info)
        print("checkout/webhookhandler save_info is above ---------***********-----------------**************------------")

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        #  to ensure that the empty fields from the form are in the format we want (none, instead of null), we give the non value below
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # update profile information if save_info was checked. this will run if the checkout/views.py > checkout does not work. to test: remove form.subit() line from stripe_elements.js file
        # to allow non authenticated users to checkout, make profile=none
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()


        order_exists = False
        # attempt is an effort to deal with delays on one the client side.
        # ...For example, if the stripe tries to get the order but the site hasn't finished doing it yet.
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                # attempt is an effort to deal with delays on one the client side.
                # ...For example, if the stripe tries to get the order but the
                # ... site hasn't finished doing it yet.

                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook to received: {event["type"]}',
            status=200
        )
