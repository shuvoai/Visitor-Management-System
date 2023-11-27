from django.urls import path
from .views import ValidateOtp

urlpatterns = [
    path(
        'validate-otp/<int:visitor_pk>',
        ValidateOtp.as_view(),
        name='validate-otp'
    ),
]
