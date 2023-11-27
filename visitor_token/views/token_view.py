import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from visitor_token.models import VisitorToken
from visitor_token.service import generate_qr_code

import pyqrcode
from io import StringIO
from io import BytesIO

import re

from reportlab.pdfgen.canvas import Canvas
# from reportlab_qrcode import QRCodeImage
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF

from reportlab.graphics.shapes import Drawing


def token_pdf_generate(request):
    token_object = VisitorToken.objects.order_by("-pk")[0]
    token = token_object.token
    token_name, visitor_name = token.split(":")
    pdf_name = token_object.token_for.visitor_name
    visitor_name = visitor_name.title().rstrip("1234567890")

    data = token_object.token

    visitor_qr_code = generate_qr_code(data)

    aamarpay_logo_img_file = 'dashboard/static/dashboard/img/aamarpay_logo.png'
    # visitor_qr_code = 'dashboard/static/dashboard/img/visitor_qr_code.png'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    PAGE_HEIGHT = p._pagesize[1]
    # p.line(40,72,40,PAGE_HEIGHT-72)
    # p.setLineWidth(5)
    p.setPageSize((350, 200))
    p.drawImage(aamarpay_logo_img_file, 30, 120, mask="auto")
    p.drawString(43, 80, token_name)
    p.drawString(43, 50, visitor_name)
    # p.drawImage(a, 300,100,mask="auto")

    # p.drawImage(visitor_qr_code,240,40,height = 80, width=80,mask=None)
    qr_code = qr.QrCodeWidget(data)
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(45, 45, transform=[80. / width, 0, 0, 80. / height, 0, 0])
    d.add(qr_code)
    renderPDF.draw(d, p, 240, 34)

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=pdf_name + '.pdf')
