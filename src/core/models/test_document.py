import mongoengine
from .tests import Test
from datetime import datetime


class TestDocument(mongoengine.Document):
    """Mongo document to store Test instance, which is an Embedded document"""
    created = mongoengine.DateTimeField(default=datetime.utcnow)
    test = mongoengine.EmbeddedDocumentField(Test)

    meta = {
        'db_alias': 'core',
        'collection': 'singleTest',
        'indexes': ['created'],
        'ordering': ['created']
    }
