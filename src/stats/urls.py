from django.urls import path
from . import views

app_name='stats'


urlpatterns = [

    path('latest/', views.latest, name='latest'),
    path('by-id/', views.byId ,name='by-id'),
    path('by-id/<testSuiteId>/', views.byIdResult, name='by-id-result'),
    path('compare/', views.compare, name='compare'),
    path('compare/<start_date>/<end_date>', views.compareResult, name='compare-result'),

    ### BOKEH GRAPHS GETTERS ####
    path('get-bokeh/<testSuiteId>', views.getBokeh, name='get-bokeh'),
    path('get-bokeh-compare/<start_date>/<end_date>', views.getBokehCompare, name='get-bokeh-compare')
]