from django.http import HttpResponse


class StripeWH_Handler:
    """Handle Stripe webhooks"""
# init runs every time a instance of this class is created
    def __init__(self, request):
        self.request = request
        print("Create 'request' from __init__ ---------***********-----------------**************------------")
        print(request)
        print("Print self: ---------***********-----------------**************------------")
        print(self)
    
    def handle_event(self, event):
        """
        Handle a generic/inknown/nuexpected webhook event
        """
        return HttpResponse(
            content=f'webhook received: {event["type"]}',
            status=200
        )