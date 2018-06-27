from django.shortcuts import render
from .models import Company,Holiday
from .models import Work_Type,Designation
from .models import Job_Type,Department
from .models import Holiday
from .forms import CompanyForm
from .forms import HolidayForm
from .forms import WorkTypeForm
from .forms import DesignationForm
from .forms import DepartmentForm
from .forms import JobTypeForm
from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url = "login")
def company_homepage(request):

    pk=request.user.employee.company.pk
    company = get_object_or_404(Company,pk=pk)
    
    return render(request,
                  'company/home.html',
                   {'company':company}
                )
@login_required(login_url = "login")
def edit_company(request):
    pk=request.user.employee.company.pk
    company = get_object_or_404(Company,pk=pk)
    if request.method == "POST":
        form=CompanyForm(request.POST,request.FILES, instance=company)
    
        
        if form.is_valid():
            company=form.save(commit=False)
            #company.logo = request.FILES['logo']
            company.save()
            messages.success(request,'Company Updated successfully')
            #request.session['company']=1
            return redirect('edit_company'# ,pk=company
            )
        else:
            messages.success(request,'Invalid Credentials')
            return redirect('add_company')
            
    else:
        form=CompanyForm(instance=company)
                
    return render(request,
                  'company/company_edit.html',
                  {'form':form}
                )
@login_required(login_url = "login")
def add_holiday(request):
    pk=request.user.employee.company
    holiday_list= Holiday.objects.filter(company=pk)
    if request.method == "POST":
        form=HolidayForm(request.POST)
        if form.is_valid():
            holiday_exist=Holiday.objects.filter(company=pk,name=request.POST['name']).exists()
            if not holiday_exist:
                holiday= form.save(commit=False)
                holiday.company=pk
                holiday.save()
                print('holiday',holiday.company)
                messages.success(request,'Holiday added successfully !')
                return render(request,'company/holiday_edit.html',
                  {'form':form,
                   'holiday_list':holiday_list}
                 )
            else:
                messages.success(request,'Holiday has been already added !')
        else:
            messages.success(request,'Invalid Credentials')
            return redirect(add_holiday)
    else:
        
        form=HolidayForm()
    return render(request,
                  'company/holiday_edit.html',
                  {'form':form,
                   'holiday_list':holiday_list}
                 )


@login_required(login_url = "login")
def holiday_detail(request):
    pk=request.user.employee.company.pk
    holiday= Holiday.objects.filter(company=pk)
    return render(request,
                  'company/holiday_detail.html',
                   {'holiday':holiday}
                 )
@login_required(login_url = "login")
def holiday_delete(request,pk):

    holiday=get_object_or_404(Holiday,pk=pk)
    holiday.delete()
    return redirect(add_holiday)
    # return render(request,'payroll/holiday_detail.html',{'action':'Deleted Successfully'}) 




@login_required(login_url = "login")
def add_worktype(request):
    pk=request.user.employee.company
    worktype_list=Work_Type.objects.filter(company = pk)
    if request.method == "POST":
        form=WorkTypeForm(request.POST)
        if form.is_valid():
            worktype_exist=Work_Type.objects.filter(company=pk,worktype=request.POST['worktype']).exists()
            if not worktype_exist:
                work_type = form.save(commit=False)
                work_type.company=pk
                work_type.save()
                messages.success(request,'Work-Type added successfully !')
                return render(request,
                              'company/worktype_edit.html',
                              {'form':form,
                               'worktype_list':worktype_list
                              }
                )
            else:
                messages.success(request,'Work-Type has been already added !')
        else:
            messages.success(request,'Invalid Credentials')
            return redirect(add_worktype)
    else:
        form=WorkTypeForm()
    return render(request,
                  'company/worktype_edit.html',
                  {'form':form,
                   'worktype_list':worktype_list
                  }
                 )

@login_required(login_url = "login")
def add_designation(request):
    pk=request.user.employee.company
    desg=Designation.objects.filter(company = pk)
    
    if request.method == "POST":
        form = DesignationForm(request.POST)
        if form.is_valid():
            designation_exist=Designation.objects.filter(company=pk,designation=request.POST['designation']).exists()
            if not designation_exist:
                designation=form.save(commit=False)
                designation.company=pk
                designation = form.save()
                messages.success(request,'Designation added successfully !')
                return render(request,
                              'company/designation_edit.html',
                              {'form':form,
                               'desg':desg
                              }
                )
            else:
                messages.success(request,'Designation has been already added !')
        else:
            messages.success(request,'Invalid Credentials')
            return redirect(add_designation)
    else:
        form=DesignationForm()
    return render(request,
                  'company/designation_edit.html',
                  {'form':form,
                   'desg':desg
                  }
                 )

@login_required(login_url = "login")
def add_department(request):
    pk=request.user.employee.company
    dept=Department.objects.filter(company = pk)
    
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department_exist=Department.objects.filter(company=pk,department=request.POST['department'])
            if not department_exist:
                department=form.save(commit=False)
                department.company=pk
                department = form.save()
                messages.success(request,'Department added successfully !')
                return render(request,
                              'company/department_edit.html',
                              {'dept':dept,
                               'form':form
                              }
                )
            else:
                messages.success(request,'Department has been already  added !')
        else:
            messages.success(request,'Invalid Credentials')
            return redirect(add_designation)
    else:
        form=DepartmentForm()
    return render(request,
                  'company/department_edit.html',
                  {'form':form,
                   'dept':dept
                  }
                 )

@login_required(login_url = "login")
def add_jobtype(request):
    pk=request.user.employee.company
    jobtype=Job_Type.objects.filter(company = pk)
    if request.method == "POST":
        form = JobTypeForm(request.POST)
        if form.is_valid():
            jobtype_exist=Job_Type.objects.filter(company = pk, jobtype=request.POST['jobtype']).exists()
            if not jobtype_exist:
                record=form.save(commit=False)
                record.company=pk
                record = form.save()
                messages.success(request,'JobType added successfully')
                return render(request,
                              'company/jobtype_edit.html',
                              {'form':form,
                               'jobtype':jobtype
                              }
                )
            else:
                messages.success(request,'Job-Type has been already added !')
        else:
            messages.success(request,'Invalid Credentials')
            return redirect(add_jobtype)
    else:
        form=JobTypeForm()
    return render(request,
                  'company/jobtype_edit.html',
                  {'form':form,
                   'jobtype':jobtype
                  }
                 )



@login_required(login_url = "login")
def worktype_detail(request):
    pk=request.user.employee.company
    worktype=Work_Type.objects.filter(company = pk)
    return render(request,
                  'company/worktype_detail.html',
                  {'worktype':worktype}
                 )

@login_required(login_url = "login")
def worktype_delete(request,pk):
     worktype=get_object_or_404(Work_Type,pk=pk)
     worktype.delete()
     return redirect(add_worktype)

@login_required(login_url = "login")
def jobtype_detail(request):
    pk=request.user.employee.company
    jobtype=Job_Type.objects.filter(company = pk)
    return render(request,
                  'company/jobtype_detail.html',
                  {'jobtype':jobtype}
                 )

@login_required(login_url = "login")
def jobtype_delete(request,pk):
    
    jobtype=get_object_or_404(Job_Type,pk=pk)
    jobtype.delete()
    return redirect(add_jobtype)

@login_required(login_url = "login")
def department_detail(request):
    pk=request.user.employee.company.pk
    dept=Department.objects.filter(company = pk)
    return render(request,
                  'company/department_detail.html',
                  {'dept':dept}
                 )
@login_required(login_url = "login")
def department_delete(request,pk):
    department=get_object_or_404(Department,pk=pk)
    department.delete()
    return redirect(add_department)

@login_required(login_url = "login")
def designation_detail(request):
    pk=request.user.employee.company
    desg=Designation.objects.filter(company = pk)
    return render(request,
                  'company/designation_detail.html',
                  {'desg':desg}
                 )

@login_required(login_url = "login")
def designation_delete(request,pk):
    desg=get_object_or_404(Designation,pk=pk)
    desg.delete()
    return redirect(add_designation)

