import logging

from .mongo_setup import global_init
from .test_suites import TestSuite
from .tests import Test
from .test_document import TestDocument

# from src.core.models.mongo_setup import global_init
# from src.core.models.test_document import TestDocument
# from src.core.models.test_suites import TestSuite
# from src.core.models.tests import Test

logger = logging.getLogger(__name__)


class TestDAO:
    """Executes queries on the DB and returns results"""

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            global_init('tests')
        except Exception as e:
            logger.error("Could not establish a connection to DB: {}".format(e))

    def getAllTestSuites(self):
        try:
            testSuites = TestSuite.objects()
            logger.info("test suits: {}".format(testSuites))
            return testSuites
        except Exception as e:
            logger.error("Error in TestDAO.getAllTestSuites: {}".format(e))

    def getRangeTestSuite(self, start_date, end_date):
        try:
            query = TestSuite.objects(created__gte=start_date,
                                     created__lte=end_date)
            logger.info("Result query from getRangeTestSuite: {}".format(query))
            return query
        except Exception as e:
            logger.error("Exception at TestDAO.getRangeTestSuite: {}".format(e))

    def getTestSuiteById(self, id: str) -> TestSuite:
        try:
            return TestSuite.objects(testSuiteId=id)[0]
        except Exception as e:
            logger.error("Exception in TestDAO.getTestSuiteById: {}".format(e))

    def getLatestTestSuite(self):
        try:
            testSuite = TestSuite.objects.order_by('-created').first()
            if testSuite is None:
                return None
            return TestDAOHelper.TestSuiteToDict(testSuite)
        except Exception as e:
            logger.error("Error in getLatestTestSuite: {}".format(e))

    def getLatestTest(self, name) -> dict:
        try:
            testDocument = TestDocument.objects(test__name=name).order_by('-created').first()
            serializedDict = TestDAOHelper().serializeTest(testDocument.test)
            serializedDict.update({'created': testDocument.created})
            return serializedDict
        except Exception as e:
            logger.error("Exception in TestDAO.getLatestTest: {}".format(e))

    def addSingleTest(self, test):
        try:
            testDocument = TestDocument()
            testDocument.test = test
            testDocument.save()
            logger.info("Adding test to test document: {}".format(test))
        except Exception as e:
            logger.error("Exception in TestDAO.addSingleTest: {}".format(e))

    def addTestToTestSuite(self, test: Test, id: str) -> bool:
        try:
            querySet = TestSuite.objects(testSuiteId=id)
            if querySet:  # if there's a TestSuite with given id in query set
                testSuite = querySet[0]  # get this TestSuite
            else:  # create new TestSuite obj in db and set id
                testSuite = TestSuite()
                testSuite.testSuiteId = id
            testSuite.tests.append(test)
            testSuite.save()
            return True
        except Exception as e:
            logger.error("Could not add test ({}) to TestSuite: {}".format(test, e))
            return False

    def addDurationToTestSuite(self, id: str, time: float):
        try:
            testSuite = self.getTestSuiteById(id)
            logger.info("Adding duration ({}s) to TestSuite: {} ".format(time, TestSuite))
            testSuite.duration = time
            testSuite.save()
        except Exception as e:
            logger.error("Exception in TestDAO.persistTestSuiteDuration: {}".format(e))

    def markTestAsFinished(self, testSuiteId: str):
        try:
            testSuite = self.getTestSuiteById(testSuiteId)
            testSuite.is_finished = True
            testSuite.save()
        except Exception as e:
            logger.error("Could not mark test suit as finished: {}".format(e))


class TestDAOHelper:

    @classmethod
    def TestSuiteToDict(cls, testSuite: TestSuite) -> dict:
        if testSuite is None:
            return
        return {
            'created': str(testSuite.created),
            'testSuiteId': str(testSuite.testSuiteId),
            'duration': testSuite.duration,
            'is_finished': testSuite.is_finished,
            'tests': [TestDAOHelper.serializeTest(test) for test in testSuite.tests]
        }

    @classmethod
    def serializeTest(cls, test: Test) -> dict:
        return {
            'test_id': str(test.test_id),
            'name': str(test.name),
            'targetEnv': str(test.targetEnv),
            'duration': test.duration,
            'err': str(test.err),
            'out': str(test.out)
        }