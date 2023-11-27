from django.urls import path

from .views import DashboardView, VisitorData, VisitorDetails

urlpatterns = [

    path('', DashboardView.as_view(), name="dashboard"),
    path('visitor-data', VisitorData.as_view(), name="visitor.data"),
    path('visitor-details', VisitorDetails.as_view(), name='visitor.details'),

]
