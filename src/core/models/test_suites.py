import mongoengine
from datetime import datetime
import logging

from .tests import Test

logger = logging.getLogger(__name__)

class TestSuite(mongoengine.Document):
    created = mongoengine.DateTimeField(default=datetime.utcnow)
    testSuiteId = mongoengine.StringField()
    tests = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Test))
    duration = mongoengine.FloatField()
    is_finished = mongoengine.BooleanField()

    meta = {
        'db_alias': 'core',
        'collection': 'TestSuite',
        'indexes': [
            'created',
            'testSuiteId',
        ],
        'ordering': ['testSuiteId']
    }