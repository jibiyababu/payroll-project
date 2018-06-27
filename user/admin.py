from django.contrib import admin
from .models import Employee
from .models import Designation_History
from .models import Department_History
from .models import Job_Type_History
from .models import Leave_History
from .models import Salary_History
from .models import Salary_Increment
# Register your models here.
admin.site.register(Employee)
admin.site.register(Designation_History)
admin.site.register(Department_History)
admin.site.register(Job_Type_History)
admin.site.register(Salary_History)
admin.site.register(Salary_Increment)
 
