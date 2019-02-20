from typing import Callable
import logging
from celery import Task, Celery
from celery.result import AsyncResult, GroupResult

logger = logging.getLogger(__name__)


class BaseTaskCls(Task):

    def run(self):
        super()


class BaseMultiTestTaskCls(Task):
    def run(self):
        super()

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

class TaskManager:

    def createSignature(self, task: Callable, command=None, multitest=False, testSuiteId=None):
        """
        Create Celery signature for task(Callable).
        """
        if command is None:
            return task.s()
        if multitest:
            return task.s(command=command,
                          testSuiteId=testSuiteId,
                          multitest=multitest)
        return task.s(command)

    def startTask(self, taskSignature):
        return taskSignature.delay()

    def revoke(self):
        if self.result is not None:
            self.result.revoke(terminate=True, signal='SIGKILL')  # terminate=True <- stop already executing task

    def collectResult(self, result: GroupResult):
        """
        Store locally and temporary GroupResult of startAllTestsTask
        to revoke task execution.
        """
        self.result = result
