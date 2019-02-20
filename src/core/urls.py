from django.urls import path
from . import views

app_name='core'

urlpatterns = [

    path('', views.index, name='home'),
    path('tests/', views.tests, name='tests'),
    path('tests/run', views.run, name='run'),

    ### URL FOR FUNCTIONS THAT LAUNCH AND MANAGE TEST SCRIPTS
    path('tests/run/all', views.runAllStart, name='runAllStart'),
    path('tests/run/<script>', views.runSingleTest, name='runSingleTest'),
    path('tests/run/all/cancel', views.cancelAllTests, name='cancelAllTests'),
    path('tests/mark-as-started/', views.markAsStarted, name='markAsStarted'),
    path('tests/mark-as-finished/', views.markAsFinished, name='markAsFinished'),
]
