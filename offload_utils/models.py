from django.db import models
from jsonfield import JSONField


FILE = 1
CALLBACK = 2

DATA_TYPE_CHOICES = (
    (FILE, 'File Type'),
    (CALLBACK, 'Callback Type'),
)


class OffloadedTask(models.Model):

    function = models.ForeignKey('RegisteredOffloadableFunction')
    start_timestamp = models.DateTimeField(auto_now_add=True)
    finished_timestamp = models.DateTimeField(null=True, blank=True)
    celery_task_id = models.CharField(max_length=255)
    data_type = models.IntegerField(choices=DATA_TYPE_CHOICES)
    extras = JSONField(null=True, blank=True)


class RegisteredOffloadableFunction(models.Model):

    function = models.TextField()
