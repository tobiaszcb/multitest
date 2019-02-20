import mongoengine

class Test(mongoengine.EmbeddedDocument):
    test_id = mongoengine.StringField()
    name = mongoengine.StringField()
    targetEnv = mongoengine.StringField()
    duration = mongoengine.FloatField()
    err = mongoengine.StringField()
    out = mongoengine.StringField()

    meta = {
        'db_alias': 'core',
        'collection': 'test',
        'indexes': [
            'id',
            'name',
            'duration',
        ],
        'ordering': ['id'],
    }
