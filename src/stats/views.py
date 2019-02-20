from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from bokeh.embed import json_item

import logging

from core.models.test_dao import TestDAO
from .services.bokeh_service import BokehService
from .forms import TestSuiteIdForm, DatesToCompareForm

# from src.core.models.test_dao import TestDAO
# from src.stats.services.bokeh_service import BokehService
# from datetime import datetime, timedelta

testDAO = TestDAO()
logger = logging.getLogger(__name__)


@login_required
def latest(request):
    testSuite = testDAO.getLatestTestSuite()
    return render(request=request,
                  template_name='stats/latest.html',
                  context={'testSuiteId': testSuite['testSuiteId']})


@login_required
def byId(request):
    if request.method == "GET":
        form = TestSuiteIdForm(request.GET or None)
        if form.is_valid():
            testSuiteId = form.cleaned_data.get('test_id')
            url = reverse('stats:by-id-result', kwargs={'testSuiteId': testSuiteId})
            return HttpResponseRedirect(url)
    else:
        form = TestSuiteIdForm()
    return render(request=request,
                  template_name='stats/by_id.html',
                  context={'form': form})


@login_required
def byIdResult(request, testSuiteId):
    testSuite = request.session.get('TestSuite', None)
    logger.info("TEST SUIT FROM SESSION: {}".format(testSuite))
    return render(request=request,
                  template_name='stats/by_id_result.html',
                  context={'testSuiteId': testSuiteId})


@login_required
def compare(request):
    if request.method == "GET":
        form = DatesToCompareForm(request.GET or None)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            url = reverse('stats:compare-result', kwargs={'start_date': start_date, 'end_date': end_date})
            return HttpResponseRedirect(url)
    else:
        form = DatesToCompareForm()

    return render(request=request,
                  template_name='stats/compare.html',
                  context={'form': form})


@login_required
def compareResult(request, start_date, end_date):
    query = testDAO.getRangeTestSuite(start_date, end_date)
    ts_dict = BokehService().getCompareChartDict(query)

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'ts_dict': ts_dict
    }
    return render(request=request,
                  template_name='stats/compare_result.html',
                  context=context)

    ### BOKEH GRAPHS GETTERS ####

@login_required
def getBokeh(request, testSuiteId):
    TestSuite = testDAO.getTestSuiteById(testSuiteId)
    bokeh = BokehService()
    bokeh.feedTestSuite(TestSuite)
    figure = bokeh.getFigure()
    j_item = json_item(figure, 'myplot')
    logger.info("Returning a json_item with bokeh graph")
    return JsonResponse(j_item)


@login_required
def getBokehCompare(request, start_date, end_date):
    queryset = testDAO.getRangeTestSuite(start_date, end_date)
    bokeh = BokehService()
    ts_dict = bokeh.getCompareChartDict(queryset)
    figure = bokeh.generateBokeh(ts_dict)
    j_item = json_item(figure, 'myplot')
    return JsonResponse(j_item)
