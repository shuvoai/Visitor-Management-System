from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from visitormanagement.models import Visitors
from visitormanagement.serializers import VisitorSerializer, VisitorDetailSerializer
from django.shortcuts import redirect
from django.core import serializers
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

#
from django.shortcuts import get_object_or_404
from visitor_token.models import VisitorToken
from visitor_token.serializers import VisitorTokenSerializer
from rest_framework.renderers import TemplateHTMLRenderer


class VisitorTokenAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        visitor_token = VisitorToken.objects.order_by("-pk")[0]
        serializer = VisitorTokenSerializer(visitor_token)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = VisitorTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
