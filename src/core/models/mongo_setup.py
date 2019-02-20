import mongoengine


def global_init(db_name: str):
    mongoengine.register_connection(
        alias='core',
        name=db_name,
        username='user',
        password='user',
        authentication_source='tests',
        host='db' # delete this line if you're not using docker
    )