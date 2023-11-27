from django.urls import path

from .views import VisitorTokenAPIView, token_pdf_generate

# from .token_pdf import token_pdf_generate


urlpatterns = [
    path('api/', VisitorTokenAPIView.as_view(), name="tokenapi"),
    path('tokenpdf/', token_pdf_generate, name="tokenpdf"),

]
