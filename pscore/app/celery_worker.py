"""
Created on Mon Dec 7 17:28:15 2018

@author: Amey Bhadkamkar
"""

from celery import Celery


def make_celery(app1):
    # celery_obj = Celery(app1.import_name, backend=app1.config['CELERY_RESULT_BACKEND'],broker=app1.config['CELERY_BROKER_URL'])

    celery_obj = Celery(
        app1.import_name, broker=app1.config['CELERY_BROKER_URL'])
    celery_obj.conf.update(app1.config)
    TaskBase = celery_obj.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app1.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery_obj.Task = ContextTask

    print('Created Celery Object')

    return (celery_obj)
