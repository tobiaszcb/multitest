import logging

from ..models.tests import Test
from ..models.test_dao import TestDAO

logger = logging.getLogger(__name__)
testDao = TestDAO()


class DataCollector:
    """A layer to collect data from tests results"""

    @classmethod
    def grabData(cls, id: str, cmd: str, duration: float, err: str, out: str, multitest=False):
        # cmdList = [cd, _, _, _, python3, scriptName, cfg, _, _, xml]
        logger.info("Received data: id:{},\n name:{}\ncommand: {},\n duration: {},\n err: {}\n out: {}"
                    .format(id, cmd[4], cmd, duration, err, out))
        cmdList = cmd.split()
        logger.info(cmdList)
        name = cmdList[4].split('.')[0]  # name.py -> name
        targetEnv = cmdList[5]

        test = Test()
        test.test_id = id
        test.name = name
        test.targetEnv = targetEnv
        test.duration = duration
        test.err = err
        test.out = out

        if multitest:
            testDao.addTestToTestSuite(test, id)  # add every test to DB
        else:
            testDao.addSingleTest(test)

    @classmethod
    def grabTestSuiteDuration(cls, id: str, time: float):
        logger.info("DataCollector.grabTestSuiteDuration - id: {}, duration: {}s".format(id, time))
        testDao.addDurationToTestSuite(id, time)  # add duration of whole test suit to DB
