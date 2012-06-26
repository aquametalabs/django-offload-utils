import json

from annoying.decorators import ajax_request
from celery.result import AsyncResult
from django.shortcuts import get_object_or_404

from offload_utils.models import RegisteredOffloadableFunctionSet, OffloadedTask
from offload_utils.utils import import_class
from offload_utils.tasks import offload_wrapper


@ajax_request
def start_offload(request):
    success = True
    error_message = False
    function_name = request.POST['function_name']
    uid = request.POST['uid']
    try:
        offloadable_function_meta = RegisteredOffloadableFunctionSet.objects.get(name=function_name)
    except RegisteredOffloadableFunctionSet.DoesNotExist:
        success = False
        error_message = '%s has not been registered.' % function_name
        return {'success': success, 'error_message': error_message}
    callable = import_class(offloadable_function_meta.function)
    extras = json.loads(request.POST['extras'])
    task_res = offload_wrapper.delay(callable, **extras)
    OffloadedTask.objects.filter(uid=uid).update(stale=True)
    task = OffloadedTask.objects.create(function=offloadable_function_meta,
            celery_task_id=task_res.task_id, data_type=request.POST['datatype'],
            extras=request.POST['extras'], uid=uid
            )
    return {'success': success, 'error_message': error_message}


@ajax_request
def check_status(request):
    completed = False
    success = False
    status = None
    uid = request.POST['uid']
    try:
        offload_task = OffloadedTask.objects.get(stale=False, uid=uid)
    except OffloadedTask.DoesNotExist:
        offload_task = None
    if offload_task:
        ret = {}
        celery_task = AsyncResult(task_id=offload_task.celery_task_id)
        if celery_task.status == 'SUCCESS':
            completed = True
            success = True
            status = celery_task.status
            callable = import_class(offload_task.function.retriever)
            ret['file_url'] = callable(**offload_task.extras)
        elif celery_task.status == 'STARTED':
            completed = False
            success = True
            status = celery_task.status
        else:
            completed = False
            success = False
            status = celery_task.status
        ret['completed'] = completed
        ret['success'] = success
        ret['status'] = status
        ret['uid'] = uid
        ret['finished_timestamp'] = offload_task.finished_timestamp if offload_task else None
        ret['has_task'] = bool(offload_task or False)
        return ret
    success = True
    return {
        'completed': completed,
        'success': success,
        'status': status,
        'uid': uid,
        'has_task': bool(offload_task or False),
    }
