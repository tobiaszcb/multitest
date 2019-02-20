from django.urls import path
from .views import GetLatestTestSuite, GetLatestTest

urlpatterns = [
    path('get-latest-test-suite/',
         GetLatestTestSuite.as_view(),
         name='getLatestTestSuite'),
    path('get-latest-test/<name>/',
         GetLatestTest.as_view(),
         name='getLatestTest'),
]