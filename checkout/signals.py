# this file is meant to update the total cost wach time a line item is added. 
# ...It will do it by calling the method to update total found
# ...on the models.property()
from django.db.models.signals import post_save, post_delete
# to receive signals
from django.dispatch import receiver

from .models import OrderLineItem


# update order total on lineitem update/create
# to execute function call a receiver
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    sender = signal sender = orderline_item
    instace = instance of the model that sent it
    created = boolean sent from by django that says if the instace is new or being updated
    kwargs = key word arguments
    """
    instace.order.update_total()


# update order total on lineitem delete
@receiver(post_delete, sender=OrderLineItem)
def update_on_delte(sender, instance, **kwargs):

    instace.order.update_total()
# Next: there is a need to overight the ready method in apps.py