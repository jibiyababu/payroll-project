from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from .models import Employee
from .forms import EmployeeForm
# Create your views here.
def employee_list(request):
    emp=Employee.objects.all()
    return render(request, 'payroll/employee_list.html', {'emp':emp})
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'payroll/employee_detail.html', {'employee':employee})
def employee_new(request):
    #form = EmployeeForm()
    #return render(request, 'payroll/employee_edit.html', {'form': form})
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            #employee.name = request.user
            #post.published_date = timezone.now()
            employee.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    return render(request, 'payroll/employee_edit.html', {'form': form})
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            #post.author = request.user
            #post.published_date = timezone.now()
            employee.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'payroll/employee_edit.html', {'form': form})

