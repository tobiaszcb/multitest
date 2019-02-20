from __future__ import absolute_import, unicode_literals
from celery import shared_task, group
from subprocess import Popen, PIPE
from time import time
import logging

from .services.init_tests import TestServiceHelper
from .services.tasks_services import BaseTaskCls, BaseMultiTestTaskCls, TaskManager
from .services.collect_data_service import DataCollector
from .models.test_dao import TestDAO

testServiceHelper = TestServiceHelper()
taskMananger = TaskManager()
testDao = TestDAO()
logger = logging.getLogger(__name__)


@shared_task(base=BaseMultiTestTaskCls)
def startAllTestsTask():
    start = time()
    testSuiteId = testServiceHelper.generateId()
    scripts = testServiceHelper.getScripts()
    commands = map(testServiceHelper.getCommand, scripts)
    tasksSignatures = []
    for command in commands:
        tasksSignatures.append(
            taskMananger.createSignature(startSingleTest,
                                         command=command,
                                         multitest=True,
                                         testSuiteId=testSuiteId)
        )
    allTests = group(tasksSignatures)

    results = allTests.apply_async()

    while not results.ready():
        pass

    end = time()
    total = end - start
    total = round(total, 2)
    DataCollector.grabTestSuiteDuration(testSuiteId, total)  # add to DB
    testDao.markTestAsFinished(testSuiteId)
    return results


@shared_task(base=BaseTaskCls)
def startSingleTest(command, testSuiteId=None, multitest=False):
    """
    if multitest flag is enabled (means we're runnig whole TestSuite, not
    just a single test standalone) we'll be adding results to the DB.
    """

    start = time()
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    out, err = out.decode('utf-8'), err.decode('utf-8')
    p.terminate()

    end = time()
    total = end - start
    total = round(total, 2)
    logger.info("FINISHED TEST. CMD: {}".format(command))

    if multitest:  # add to DB
        DataCollector.grabData(testSuiteId, command, total, err, out, multitest=True)
    else:
        testId = testServiceHelper.generateId()
        DataCollector.grabData(testId, command, total, err, out, multitest=False)

    return out, err
