from django.contrib import admin

from models import *
# Register your models here.
admin.site.register(Device)
admin.site.register(Vulnerability)
admin.site.register(Reference)
admin.site.register(Cpe)
admin.site.register(Application)
admin.site.register(DeviceUpdate)
