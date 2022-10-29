from django.contrib import admin
from .models import Log, MicDataRecord

# Register your models here.
admin.site.register(MicDataRecord)
admin.site.register(Log)