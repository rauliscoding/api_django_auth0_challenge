from django.urls import path

from .views import ApplicationsDetails


urlpatterns = [
    path('applications-details', ApplicationsDetails.as_view(), name='applications-details'),
]
