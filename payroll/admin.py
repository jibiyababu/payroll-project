from django.contrib import admin
from .models import Employee
from .models import Attendance

admin.site.register(Employee)
admin.site.register(Attendance)
