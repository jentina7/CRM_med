from django.contrib import admin
from .models import *

admin.site.register(Patient)
admin.site.register(RecordingTime)
admin.site.register(Service)
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Specialty)
