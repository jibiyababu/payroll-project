from django.contrib import admin
from .models import Attendance
from .models import Leave_Application

# Register your models here.
admin.site.register(Attendance)
admin.site.register(Leave_Application)
