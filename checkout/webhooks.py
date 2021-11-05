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
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
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

    print('Success')
    return HttpResponse(status=200)
