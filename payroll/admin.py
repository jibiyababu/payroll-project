from django.contrib import admin
from .models import *
#from .models import Company
#from .models import Work_Type
#from .models import Holiday
#from .models import Designation
#from .models import Department
#from .models import Company
#from .models import Employee
#from .models import Attendance
#from .models import Salary

admin.site.register(Company)
admin.site.register(Holiday)
admin.site.register(Work_Type)
admin.site.register(Designation)
admin.site.register(Department)
admin.site.register(Job_Type)
admin.site.register(Designation_History)
admin.site.register(Department_History)
admin.site.register(Job_Type_History)
admin.site.register(Salary_History)
admin.site.register(Leave_History)
admin.site.register(Attendance)
admin.site.register(Salary)
admin.site.register(Employee)
