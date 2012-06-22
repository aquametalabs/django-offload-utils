from django.contrib import admin

from offload_utils.models import RegisteredOffloadableFunctionSet, OffloadedTask


admin.site.register(RegisteredOffloadableFunctionSet)
admin.site.register(OffloadedTask)
