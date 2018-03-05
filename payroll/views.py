from django.shortcuts import render
from .models import Employee

# Create your views here.
def employee_list(request):
    emp=Employee.objects.all()
    return render(request, 'payroll/employee_list.html', {'emp':emp})
