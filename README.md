# celery-example

## [celery](https://docs.celeryproject.org/)
### Usage
Running the Celery worker server
```
$ celery -A proj worker -l INFO
```
Starting the Scheduler
```
$ celery -A proj beat -l INFO
```
Calling the task
```
$ curl -X POST -d '{"args":[1,2]}' http://localhost:5555/api/task/async-apply/tasks.add

>>> from proj.tasks import add

>>> add.delay(2, 2)

>>> add.apply_async((2, 2))

>>> add.apply_async((2, 2), retry=True, retry_policy={
...     'max_retries': 3,
...     'interval_start': 0,
...     'interval_step': 0.2,
...     'interval_max': 0.2,
... })
<AsyncResult: faac0e46-86b2-41f9-a87f-31ef2a269c7a>

>>> res = add.delay(2, 2)
>>> res.get(timeout=1)
4
>>> res.id
d6b3aea2-fb9b-4ebc-8da4-848818db9114

>>> s1 = add.s(2, 2)
>>> res = s1.delay()
>>> res.get()
4

>>> from celery import group
>>> from proj.tasks import add
>>> group(add.s(i, i) for i in xrange(10))().get()
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

>>> from celery import chain
>>> from proj.tasks import add, mul
# (4 + 4) * 8
>>> chain(add.s(4, 4) | mul.s(8))().get()
64

>>> from celery import chord
>>> from proj.tasks import add, xsum
>>> chord((add.s(i, i) for i in xrange(10)), xsum.s())().get()
90
```

## [flower](https://flower.readthedocs.io/)
### Usage

Launch the server
```
flower -A proj --conf=proj/celeryconfig.py
```
