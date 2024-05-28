from django.urls import path

from reportingapp.views import reporting_view, generate_report_view

urlpatterns = [
    path('', reporting_view, name='reporting'),
    path('generate/', generate_report_view, name='generate_report'),
]