from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from visitormanagement.models import Visitors
from visitormanagement.serializers import VisitorSerializer, VisitorDetailSerializer
from django.shortcuts import redirect
from django.core import serializers
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from phonenumber_field.phonenumber import PhoneNumber
#
from django.shortcuts import get_object_or_404
from department.models import Department
from department.serializers import DepartmentSerializer
from rest_framework.renderers import TemplateHTMLRenderer
import sweetify
from sweetify.views import SweetifySuccessMixin
from visitormanagement.serializers import VisitorPartialUpdateSerializer
from rest_framework.permissions import AllowAny


class VisitorView(SweetifySuccessMixin, APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        visitor_phone_number = request.data.get('visitor_phone_number')
        phone_number = PhoneNumber.from_string(visitor_phone_number)
        request.data['visitor_phone_number'] = str(phone_number)

        serializer = VisitorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VisitorPartialUpdateView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VisitorPartialUpdateSerializer
    lookup_url_kwarg = 'pk'

    def patch(self, request, pk):
        visitor = self.get_object()
        serializer = self.get_serializer(
            instance=visitor,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                data=serializer.data,
                status=status.HTTP_206_PARTIAL_CONTENT
            )
        else:
            return Response(
                data={
                    "field_errors": serializer.errors
                }
            )

    def get_queryset(self):
        return Visitors.objects.all()

    def perform_update(self, serializer):
        serializer.save()
