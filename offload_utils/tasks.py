from datetime import datetime

import django.dispatch
from celery.task import task

from offload_utils.models import OffloadedTask


pre_offload = django.dispatch.Signal()
post_offload = django.dispatch.Signal(providing_args=['callable_return'])


@task
def offload_wrapper(callable, offloaded_task_id, *args, **kwargs):
    pre_offload.send(sender=offload_wrapper)
    offloaded_task = OffloadedTask.objects.get(pk=offloaded_task_id)
    ret = callable(*args, **kwargs)
    offloaded_task.finished_timestamp = datetime.now()
    offloaded_task.save()
    post_offload(sender=offload_wrapper, callable_return=ret)
