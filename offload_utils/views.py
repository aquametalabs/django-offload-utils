from annoying.decorators import ajax_request

from offload_utils.models import RegisteredOffloadableFunction, OffloadedTask
from offload_utils.utils import import_class


@ajax_request
def start_offload(request):
    print request.POST['extras']
    success = True
    error_message = False
    function_name = request.POST['function_name']
    try:
        offloadable_function_meta = RegisteredOffloadableFunction.objects.get(name=function_name)
    except RegisteredOffloadableFunction.DoesNotExist:
        success = False
        error_message = '%s has not been registered.' % function_name
        return locals()
    callable = import_class(offloadable_function_meta.function)
    task_res = callable.delay()
    task = OffloadedTask.objects.create(function=offloadable_function_meta,
            celery_task_id=task_res.task_id, data_type=request.POST['datatype'],
            )
    return {'success': success, 'error_message': error_message}


@ajax_request
def offload_status(request, celery_task_id):
    task = OffloadedTask.objects.get(celery_task_id=celery_task_id)
    return {'success': True, 'completed': False}
