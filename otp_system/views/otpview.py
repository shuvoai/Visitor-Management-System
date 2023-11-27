from rest_framework.generics import GenericAPIView
from visitormanagement.models import Visitors
from otp_system.models import Otp
from otp_system.serializers import ValidateOtpSerializer
from rest_framework.permissions import AllowAny
from otp_system.utils.generate_otp import OTPManager
from cryptography.fernet import Fernet
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from django.conf import settings
from analytics.signals import update_visitor_count


class ValidateOtp(GenericAPIView):
    queryset = Otp.objects.all()
    serializer_class = ValidateOtpSerializer
    permission_classes = [AllowAny]
    lookup_field = 'visitors'
    lookup_url_kwarg = 'visitor_pk'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            visitor_otp = self.get_object()
            generated_otp = visitor_otp.otp_code
            secret_key = settings.OTP_SECRET_KEY
            otp_manager = OTPManager(secret_key)
            otp_code = serializer.validated_data['otp_code']
            otp_status = otp_manager.validate_otp(
                submitted_otp=otp_code, generated_otp=generated_otp
            )
            if otp_status:
                visitor_otp.change_is_verified_to_true()
                visitor_otp.visitors.visitor_checkout()
                update_visitor_count()
            return Response(
                data={
                    'is_verified': otp_status
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={"field_errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
