from django.urls import path

from .views import Visitor, VisitorView, VisitorPartialUpdateView

urlpatterns = [
    path('api/', VisitorView.as_view(), name="visitorapi"),
    path('visitorform/', Visitor.as_view(), name="visitor"),
    path(
        'visitor-checkout/<int:pk>',
        VisitorPartialUpdateView.as_view(),
        name='visitor-checkout'
    )
]
