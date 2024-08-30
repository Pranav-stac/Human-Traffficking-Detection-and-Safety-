from django.contrib import admin
from .models import CustomUser, IncidentReport, SOS, SuspiciousActivity, Image

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(IncidentReport)
admin.site.register(SOS)

admin.site.register(SuspiciousActivity)
admin.site.register(Image)


