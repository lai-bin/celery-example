from proj.celery import app
import requests
from celery.utils.log import get_task_logger
from requests.exceptions import RequestException
from celery import Task
from celery.exceptions import Reject

logger = get_task_logger(__name__)


@app.task(name='sum-of-two-numbers')
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task(bind=True)
def dump_context(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.
          format(self.request))


@app.task(bind=True, default_retry_delay=10)  # retry in 30 minutes.
def add_retry(self, x, y):
    try:
        raise Exception('add error')
    except Exception as exc:
        # overrides the default delay to retry after 1 minute
        raise self.retry(exc=exc, countdown=2)


@app.task(autoretry_for=(RequestException, ), retry_kwargs={'max_retries': 5})
def autoretry_for_request_exception():
    return requests.get('https://google.com', timeout=1)


class MyTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


class BaseTaskWithRetry(Task):
    autoretry_for = (TypeError, )
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = False


@app.task(base=MyTask)
def add_my_task(x, y):
    raise TypeError()


@app.task(bind=True, acks_late=True)
def requeues(self):
    if not getattr(self.request, 'redelivered', False):
        raise Reject('no reason', requeue=True)
    print('received two times')
