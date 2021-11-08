# bellow to get the webhook and stripe api secrets
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
#  since stripe dont send the csrf, we gotta get it. below
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe


@require_POST
@csrf_exempt
# code below come from stripe with some modifications
def webhook(request):
    print("request = ---------***********-----------------**************------------")
    print(request)
    print('request end')
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    print("sig_header = ---------***********-----------------**************------------")
    print(sig_header)
    print('sig_header end')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(content=e, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(content=e, status=400)
    # exception to handle generic errors below
    except Exception as e:
        return HttpResponse(content=e, status=400)

    print('success')

    # Set up a webhook handler
    # Creating an instance
    handler = StripeWH_Handler(request)
    print("handler = StripeWH_Handler(request) = ---------***********-----------------**************------------")   
    print(handler)
    print('handler end')

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    event_type = event['type']
    print("event_type = ---------***********-----------------**************------------")   
    print(event_type)
    print('event_type end')

    # If there's a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)
    print("event_handler = ---------***********-----------------**************------------")   
    print(event_handler)
    print('event_handler end')

    # Call the event handler with the event
    response = event_handler(event)
    print("response = event_handler(event) = ---------***********-----------------**************------------")   
    print(response)
    print('response = event_handler(event) end')

    return response
