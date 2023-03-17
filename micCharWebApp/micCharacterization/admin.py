from django.contrib import admin
from .models import Log, MicDataRecord

admin.site.register(MicDataRecord)
admin.site.register(Log)