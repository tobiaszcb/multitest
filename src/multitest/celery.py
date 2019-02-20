from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multitest.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('multitest')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# Think about creating task factory. Check again task signature.
# Think about assigning tasks to a group/chain and how to control them
# so they don't fire all at once. We'd like to cancel them somehow
# and go back (if we change page) to see their execution. Think about websockets maybe I dunno.
# Read more about multiprocessing. Celery is kinda async, but can also execute code synchronously.
