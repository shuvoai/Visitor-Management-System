from .views import AnalyticsView, Visitor_details_by_date_search, Visitor_details_by_date_search_report, visitor_details_all_report, ResonWiseVisitorChart, VisitorDetailsExcelExport, NumberofVisitorsPerMonth, DepartmentWiseVisitorChart

from django.urls import path

urlpatterns = [
    path('', AnalyticsView.as_view(), name="analyticsview"),
    path('visitor_details_by_date_search', Visitor_details_by_date_search.as_view(), name="visitor_details_by_date_search"),
    path('visitor_details_by_date_search_report', Visitor_details_by_date_search_report.as_view(), name="visitor_details_by_date_search_report"),
    path('visitor_details_all_report', visitor_details_all_report.as_view(), name="visitor_details_all_report"),
    path('resonWise-visitor-chart', ResonWiseVisitorChart.as_view(), name="resonwisevisitorchart"),
    path('departmentWise-visitor-chart', DepartmentWiseVisitorChart.as_view(), name="departmentWisevisitorchart"),
    path('visitor-details-excel-export', VisitorDetailsExcelExport.as_view(), name="visitordetailsexcelexport"),
    path('number-of-visitors-per-month', NumberofVisitorsPerMonth.as_view(), name="number_of_visitors_per_month")
]
