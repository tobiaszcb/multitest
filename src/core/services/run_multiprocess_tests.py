import os
from time import time
from subprocess import Popen, PIPE
from multiprocessing import Pool, cpu_count

from .init_tests import TestServiceHelper
from .collect_data_service import DataCollector


class RunMultiTest:
    """Used before switching to celery tasks"""

    def __init__(self):
        self.testHelper = TestServiceHelper()
        self.id = self.testHelper.generateId()

    def getId(self):
        return self.id

    def shouldLaunchTestAgain(self, cmd, err):
        if (
                "TimeoutException" in err or
                "ElementClickInterceptedException" in err or
                "StaleElementReferenceException" in err or
                "BadStatusLine" in err
        ):
            print("Launching {} again...".format(cmd[4]))
            self.worker(cmd, didLaunchOnce=True)

    def worker(self, cmd:list, didLaunchOnce=False):
        start = time()
        p = Popen(
            cmd,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True
        )
        out, err = p.communicate()

        # if test failed once, we'll launch it again (but only once)
        # if it passes, then great. Else we'll return 'something'(eg. PID of that process) from child process
        # in order to keep track of how many test failed
        if len(err) != 0:
            if not didLaunchOnce:
                self.shouldLaunchTestAgain(cmd, err)
                return os.getpid()
            print("[ERROR]")
            print(err)
        p.terminate()

        end = time()
        total = end - start
        DataCollector.grabData(self.id, cmd, total, err)

    def runAllTests(self):
        start = time()
        pool = Pool(cpu_count() - 1)
        results = pool.map(self.worker, self.testHelper.commandList)
        pool.close()
        pool.join()

        total = time() - start
        total = round(total, 2)
        numOfErrs = len([i for i in results if i is not None])
        numOfTests = len(self.testHelper.scripts)
        numOfPassedTests = numOfTests - numOfErrs

        print("Czas wykonania się testów: {:.2f}s".format(total))
        print("Poprawnie wykonało się {} na {} testów.".format(numOfPassedTests, numOfTests))
        print("Liczba testów, które zakończyły się niepowodzeniem: {}".format(numOfErrs))
        DataCollector.grabTestSuiteDuration(self.id, total)
