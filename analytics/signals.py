from visitormanagement.models import Visitors
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Visitors)
def change_visitor_on_site(sender, instance, created, **kwargs):
    if created:
        update_visitor_count()


def update_visitor_count():
    visitors_on_site = Visitors.objects.visitors_on_site().count()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "analytics",
        {
            "type": "update_visitor_count",
            "visitor_count": visitors_on_site
        }
    )
