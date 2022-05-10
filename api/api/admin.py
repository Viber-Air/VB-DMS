from django.contrib import admin
from .models import RawData, DataBatch

# Register your models here.

admin.site.register(RawData)
admin.site.register(DataBatch)
