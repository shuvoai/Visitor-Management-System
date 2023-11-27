from django.db.models.signals import post_save
from django.dispatch import receiver
from visitormanagement.models import Visitors
from visitor_token.models import VisitorToken

from datetime import datetime, timezone

# test codes
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


@receiver(post_save, sender=Visitors)
def token_handler(sender, instance, created, **kwargs):
    if created:
        current_time = datetime.now(timezone.utc)
        token = instance.visitor_date.strftime("%B")[:3].upper() + "-AAP-" + instance.visitor_date.astimezone(
        ).strftime("%H%M") + ":" + instance.visitor_name.upper() + str(instance.pk)
        # shows incorrect time , fix later
        VisitorToken.objects.create(token_for=instance, token=token)


@receiver(post_save, sender=Visitors)
def token_pdf_generate_handler(sender, instance, created, **kwargs):
    if created:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        token_object = VisitorToken.objects.order_by("-pk")[0]
        token = token_object.token
        pdf_name = token_object.token_for.visitor_name

        p.drawString(100, 100, token)
        p.showPage()
        p.save()
        buffer.seek(0)
        # breakpoint()
        return FileResponse(buffer, as_attachment=True, filename=pdf_name + '.pdf')
