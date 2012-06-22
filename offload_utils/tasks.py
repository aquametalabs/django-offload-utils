from django.conf import settings

from celery.task import task
import telegram


@task
def offload_wrapper(callable, *args, **kwargs):
    ret = callable(*args, **kwargs)
    if (getattr(settings, 'OFFLOAD_UTILS_NOTIFICATIONS', False) and 
            getattr(settings, 'OFFLOAD_UTILS_TELEGRAM_CHANNEL', False) and
            ret.has_key('telegram_subject') and
            ret.has_key('telegram_content')):
        telegram_extras = {}
        if kwargs.has_key('telegram_extras'):
            telegram_extras = kwargs['telegram_extras']
        telegram.broadcast(
            settings.OFFLOAD_UTILS_TELEGRAM_CHANNEL,
            ret['telegram_subject'],
            ret['telegram_content'],
            add_to_queue=False,
            **telegram_extras)
