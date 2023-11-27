import pyqrcode
from io import StringIO
from io import BytesIO


def generate_qr_code(data):
    ############
    byte_instance = BytesIO()
    ##########
    # data = bytes(data, 'utf-8')
    qrcode = pyqrcode.create(data)
    qrcode.png("qrcode.png", scale=8)
    # breakpoint()
    # qrcode_for_token =  byte_instance.getvalue()
    # breakpoint()
    return qrcode.code
