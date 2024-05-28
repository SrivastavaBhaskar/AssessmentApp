from django.urls import path

from assessmentapp.views import assessment_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('assessment/', assessment_view, name='assessment'),
]