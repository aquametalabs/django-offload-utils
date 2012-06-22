from django.db import models
from jsonfield import JSONField


FILE = 1
CALLBACK = 2

DATA_TYPE_CHOICES = (
    (FILE, 'File Type'),
    (CALLBACK, 'Callback Type'),
)


class OffloadedTask(models.Model):

    function = models.ForeignKey('RegisteredOffloadableFunctionSet')
    uid = models.CharField(max_length=255)
    start_timestamp = models.DateTimeField(auto_now_add=True)
    finished_timestamp = models.DateTimeField(null=True, blank=True)
    celery_task_id = models.CharField(max_length=255)
    data_type = models.IntegerField(choices=DATA_TYPE_CHOICES)
    extras = JSONField(null=True, blank=True)
    stale = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s: %s' % (self.function.name, self.start_timestamp)


class RegisteredOffloadableFunctionSet(models.Model):

    name = models.CharField(max_length=128)
    function = models.TextField()
    retriever = models.TextField()
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.name
