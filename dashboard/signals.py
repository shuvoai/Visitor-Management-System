from visitormanagement.models import Visitors
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


@receiver(post_save, sender=Visitors)
def broadcast_visitor_add_notification(sender, instance, created, **kwargs):
    if created:
        visito_name = instance.visitor_name
        organization = instance.visitor_organization
        purpose = instance.visitor_purpose
        to_which_department = instance.to_which_department
        message = "A new visitor named {} has come. Organization = {}, Reason = {}, Department = {}".format(
            visito_name,
            organization,
            purpose,
            to_which_department
        )
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)("notifications", {
            "type": "notification_sender", "message": message})
