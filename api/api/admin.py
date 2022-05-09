from django.contrib import admin
from .models import Module, RawData, DataBatch

# Register your models here.

admin.site.register(Module)
admin.site.register(RawData)
admin.site.register(DataBatch)
