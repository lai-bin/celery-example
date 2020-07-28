from celery.schedules import crontab

## Broker settings.
broker_url = 'amqp://guest:guest@localhost:5672//'
# broker_url = 'redis://'

# A sequence of modules to import when the worker starts.
include = ('proj.tasks', )

## Using the database to store task state and results.
result_backend = 'db+sqlite:///results.db'

task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

worker_concurrency = 2

result_expires = 3600

beat_schedule = {
    'add-every-30-seconds': {
        'task': 'celeryproject.tasks.add',
        'schedule': 30.0,
        'args': (423,25)
    },
    'multiply-at-some-time': {
        'task': 'celeryproject.tasks.add',
        'schedule': crontab(hour=16, minute=5),
        'args': (234,63245)
    }
}

## flower
port = 5555

