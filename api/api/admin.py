from django.contrib import admin
from .models import UserProfile, Module, RawData

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Module)
admin.site.register(RawData)
