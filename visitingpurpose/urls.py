from django.urls import path
from .views import VisitingPurposeView, VisitingPurposeUpdateView, VisitingPurposeDeleteView, VisitingPurposeAPIView, ReasonDataTable, reasoneDelete

urlpatterns = [

    path('api/', VisitingPurposeAPIView.as_view(), name="visitingpurposeapi"),
    #
    path('', VisitingPurposeView.as_view(), name="visitingpurpose"),
    path('table/', ReasonDataTable.as_view(), name='reason.table'),
    path('update/<pk>', VisitingPurposeUpdateView.as_view(),
         name="visitingpurposeupdatetview"),
    path('delete/<pk>', VisitingPurposeDeleteView.as_view(),
         name="visitingpurposedeleteview"),
    path('reason-delete/<int:reason_id>',
         reasoneDelete, name='reason.delete')

]
