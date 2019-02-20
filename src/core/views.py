from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import logging

from .services.tasks_services import TaskManager
from .services.init_tests import TestServiceHelper
from .tasks import startAllTestsTask, startSingleTest

logger = logging.getLogger(__name__)
taskManager = TaskManager()
testServiceHelper = TestServiceHelper()


@login_required
def index(request):
    return render(request, template_name='core/index.html')


@login_required
def tests(request):
    scripts = testServiceHelper.getScripts()
    scripts_ids = [i for i in range(len(scripts))]
    scripts = [script.split(".")[0] for script in scripts]  # get rid of '.py'

    return render(
        request=request,
        template_name='core/tests.html',
        context= {'scripts': zip(scripts, scripts_ids)}
    )


@login_required
def run(request: WSGIRequest):
    context = {'should_launch': True}
    is_running = request.session.get('is_running','')
    logger.info("FROM RUN: IS RUNNING {}".format(is_running))
    if is_running:
        context['should_launch'] = False
    return render(request=request,
                  template_name='core/run.html',
                  context=context)


### TEST SCRIPT LAUNCHERS ###

@login_required
def runAllStart(request: WSGIRequest):
    signature = taskManager.createSignature(startAllTestsTask)
    result = taskManager.startTask(signature)  # GroupResult
    taskManager.collectResult(result)
    return HttpResponse("Launched all tests")

@login_required
def runSingleTest(request: WSGIRequest, script):
    logger.info("Launching single test: {}".format(script))
    script += '.py'
    cmd = testServiceHelper.getCommand(script)
    taskSignature = taskManager.createSignature(startSingleTest, command=cmd)
    taskManager.startTask(taskSignature)  # fire acutal task

    return HttpResponse("Launching %s" % script)

@login_required
def cancelAllTests(request):
    try:
        taskManager.revoke()
    except Exception as e:
        print("Exception in cancelAllTests: ", e)
    return HttpResponse("REVOKED")

@login_required
def markAsStarted(request):
    """
    It's being called inside run.html after launching all tests, to prevent
    launching scripts again (for example after refreshing.
    After launching tests, 'is_running' is set to True in session.
    """
    request.session['is_running'] = True
    return HttpResponse("IS_RUNNING = TRUE")

@login_required
def markAsFinished(request):
    request.session['is_running'] = False
    return HttpResponse("IS_RUNNING = FALSE")