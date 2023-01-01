from django.contrib import admin
from .models import Log, MicDataRecord, TemporalDatabase, SpectralDatabase

# Register your models here.
admin.site.register(MicDataRecord)
admin.site.register(Log)
admin.site.register(TemporalDatabase)
admin.site.register(SpectralDatabase)