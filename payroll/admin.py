from django.contrib import admin
from .models import Employee
from .models import Attendance
from .models import Salary

admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Salary)
