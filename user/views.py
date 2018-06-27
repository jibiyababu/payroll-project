from .models import Employee,Designation_History
from django.utils import timezone
from .models import Department_History
from .models import Job_Type_History
from.models import Salary_History,Salary_Increment
from company.models import Department
from .forms import EmployeeForm,SalaryForm,UserForm
from .forms import DepartmentForm,JobTypeForm
from .forms import DesignationForm,SalaryIncrementForm
from django.contrib.auth.models import User
from company.models import Company
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import datetime
# Create your views here.

@login_required(login_url = "login")
def employee_list(request):
    company=request.user.employee.company.pk
    emp = Employee.objects.filter(company=company)
    
    return render(request, 'payroll/employee_list.html', {'emp':emp})

@login_required(login_url = "login")
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    date = datetime.datetime.now().date()
    try:
        desgn = Designation_History.objects.filter(employee=pk).latest('id')
        print(desgn)
    except:
        desgn=None
    try:    
        dept = Department_History.objects.filter(employee=pk).latest('id')
    except:
        dept=None
    try:
        jobtype = Job_Type_History.objects.filter(employee=pk).latest('id')
    except:
        jobtype=None
    try:
        annual_salary=Salary_Increment.objects.filter(employee=pk,effective_from__lte=date).latest('id')
        
    except:
        annual_salary=None
    try:
        salary = Salary_History.objects.filter(employee=pk).latest('id')
    except:
        salary=None
    return render(request, 'payroll/employee_detail.html',
                  {'employee':employee,
                   'desgn':desgn,
                   'dept':dept,
                   'jobtype':jobtype,
                   'salary':salary,
                   'annual_salary':annual_salary
    })

@login_required(login_url = "login")
def employee_new(request):

    company=request.user.employee.company
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        desgform=DesignationForm(company,request.POST)
        deptform=DepartmentForm(company,request.POST)
        jobtypeform=JobTypeForm(company,request.POST)
        salaryform=SalaryForm(request.POST)

        if form.is_valid():
            employee = form.save()
            

            designation = desgform.save(commit=False)
            print("designation",designation)
            designation.employee=employee
            designation.date=datetime.datetime.now().date()
            print("designation emp",designation.employee) 
            designation.save()

            department = deptform.save(commit=False)
            department.employee=employee
            department.date=datetime.datetime.now().date()
            department.save()

            jobtype = jobtypeform.save(commit=False)
            jobtype.employee=employee
            jobtype.date=datetime.datetime.now().date()
            jobtype.save()

            
            salary = salaryform.save(commit=False)
            salary.date=datetime.datetime.now().date()
            salary.employee=employee
            salary.save()
            print('salary',salary)
            messages.success(request,'Updated successfully')
            return redirect('employee_detail', pk=employee.pk)
        else:
            messages.success(request,'Invalid Credentials')

    else:
        form = EmployeeForm()
        desgform=DesignationForm(company)
        deptform=DepartmentForm(company)
        jobtypeform=JobTypeForm(company)
        salaryform=SalaryForm()
    return render(request, 'payroll/employee_edit.html',
                  {'form': form,
                   'desgform':desgform,
                   'jobtypeform':jobtypeform,
                   'deptform':deptform,
                   'salaryform':salaryform
    })

# this view updates employee profile
@login_required(login_url = "login")
def employee_edit(request, pk):

    employee = get_object_or_404(Employee, pk=pk)
    company=request.user.employee.company
    print('emp',employee.name)
    data={
        'name':employee.name
    }
    try:

        desgn = Designation_History.objects.filter(employee=pk).latest('id')
        
        desgn_data={
                 'date':desgn.date,
                 'designation':desgn.designation_id,
                 'employee':desgn.employee
                   }

    except ObjectDoesNotExist:

        desgn=None
        desgn_data={
                 'date':None,
                 'designation':None,
                 'employee':None
                   }
    try:

        dept = Department_History.objects.filter(employee=pk).latest('id')
        dept_data={
                 'date':dept.date,
                 'department':dept.department_id,
                 'employee':dept.employee
    }
        
    except:

        dept_data={
                 'date':datetime.datetime.now().date(),
                 'department':None,
                 'employee':employee.pk
                   }
        
   
    try:
         jobtype = Job_Type_History.objects.filter(employee=pk).latest('id')
         jobtype_data={
                 'date':jobtype.date,
                 'job_type':jobtype.job_type_id,
                 'employee':jobtype.employee
                 
                     }

    except:

        jobtype_data={
                 'date':datetime.datetime.now().date(),
                 'job_type':None,
                 'employee':employee.pk
                 
                     }

    # try:

    #     salary = Salary_History.objects.filter(employee=pk).latest('id')
    #     salary_data={
    #              'date':salary.date,
    #              'employee':salary.employee,
    #              'basic_percentage':salary.basic_percentage,
    #              'hra_percentage':salary.hra_percentage,
    #              'conveyance_allowance':salary.conveyance_allowance,
    #              'special_allowance':salary.special_allowance,
    #              'proffessional_tax':salary.proffessional_tax,
    #              'income_tax':salary.income_tax
    #                   }

    # except:

    #     salary_data={
    #              'date':datetime.datetime.now().date(),
    #              'employee':employee.pk
                 
    #                 }
    #print('profile_pic',employee.profile_pic)
    if request.method == "POST" :
        
        form = EmployeeForm(request.POST,request.FILES,instance=employee)
        print('form',request.FILES)
        
    
        desgform=DesignationForm(request.POST)
        deptform=DepartmentForm(request.POST)
        jobtypeform=JobTypeForm(request.POST)
        #salaryform=SalaryForm(request.POST)
        print('form',form.is_bound)
        if form.is_valid() and desgform.is_valid() and deptform.is_valid() and jobtypeform.is_valid():
            print('file',desgform.errors)    
            form.save()
            
            designation = desgform.save(commit=False)
            designation.employee=employee
            designation.date=datetime.datetime.now().date() 
            designation.save()
            
            department = deptform.save(commit=False)
            department.employee=employee
            department.date=datetime.datetime.now().date()
            department.save()

            jobtype = jobtypeform.save(commit=False)
            jobtype.employee=employee
            jobtype.date=datetime.datetime.now().date()
            jobtype.save()

            
            # salary = salaryform.save(commit=False)
            # salary.date=datetime.datetime.now().date()
            # salary.employee=employee
            # salary.save()
            
            messages.success(request,'Updated successfully')
            return redirect('employee_detail', pk=employee.pk)

        else:
            messages.success(request,'Invalid Credentials')

    else:
        print('emp',employee.name)
        form = EmployeeForm(instance=employee)
        print(form)
        desgform=DesignationForm(company=company,initial=desgn_data)
        deptform=DepartmentForm(company=company,initial=dept_data)
        jobtypeform=JobTypeForm(company=company,initial=jobtype_data)
        #salaryform=SalaryForm(initial=salary_data)

    return render(request, 'payroll/employee_edit.html',
                  {'form': form,
                   'desgform':desgform,
                   'jobtypeform':jobtypeform,
                   'employee':employee,
                   'deptform':deptform
         
    })

#this view updates admin profile
@login_required(login_url = "login")
def admin_edit(request):
    
    company=request.user.employee.company
    employee=request.user.employee
    #admin=Employee.objects.filter(company=company,is_admin=True)
    admin = get_object_or_404(Employee,company=company.pk, is_admin=True)
    try:
        
        desgn = Designation_History.objects.filter(employee=admin.pk).latest('id')
        desgn_data={
                 'date':desgn.date,
                 'designation':desgn.designation_id,
                 'employee':desgn.employee
    }
    except:
        desgn_data=None
    try:
        dept = Department_History.objects.filter(employee=admin.pk).latest('id')
        dept_data={
                 'date':dept.date,
                 'department':dept.department_id,
                 'employee':dept.employee
    }
    except:
        dept_data=None
    try:
        jobtype = Job_Type_History.objects.filter(employee=admin.pk).latest('id')
        jobtype_data={
                 'date':jobtype.date,
                 'job_type':jobtype.job_type_id,
                 'employee':jobtype.employee
                 
    }
    except:
        jobtype_data=None
    # try:
    #     salary = Salary_History.objects.filter(employee=admin.pk).latest('id')
    #     salary_data={
    #              'date':salary.date,
    #              'employee':salary.employee,
    #              'basic_percentage':salary.basic_percentage,
    #              'hra_percentage':salary.hra_percentage,
    #              'conveyance_allowance':salary.conveyance_allowance,
                 
    #              'proffessional_tax':salary.proffessional_tax,
    #              'income_tax':salary.income_tax,
    # }
    # except:
    #     salary_data=None
    
    
    
    
    if request.method == 'POST':
        form=EmployeeForm(request.POST,instance=admin)
        desgform=DesignationForm(request.POST)
        deptform=DepartmentForm(request.POST)
        jobtypeform=JobTypeForm(request.POST)
        salaryform=SalaryForm(request.POST)
        print("designation",request.POST['designation'])
        print(form.is_valid())
        if form.is_valid():
            
            admin = form.save(commit=False)
            admin.profile_pic = request.POST['profile_pic']
            admin.save()
            
            designation = desgform.save(commit=False)
            print("designation",designation)
            designation.employee=employee
            designation.date=datetime.datetime.now().date()
            print("designation emp",designation.employee) 
            designation.save()

            department = deptform.save(commit=False)
            department.employee=employee
            department.date=datetime.datetime.now().date()
            department.save()

            jobtype = jobtypeform.save(commit=False)
            jobtype.employee=employee
            jobtype.date=datetime.datetime.now().date()
            jobtype.save()

            
            # salary = salaryform.save(commit=False)
            # salary.date=datetime.datetime.now().date()
            # salary.employee=employee
            # salary.save()


            
            messages.success(request,'Updated successfully')
            
        else:
            messages.success(request,'Invalid Credentials')
             
    else:
        form=EmployeeForm(instance=admin)
        desgform=DesignationForm(company=company,initial=desgn_data)
        deptform=DepartmentForm(company=company,initial=dept_data)
        jobtypeform=JobTypeForm(company=company,initial=jobtype_data)
        #salaryform=SalaryForm(initial=salary_data)
    return render(request,
                  'payroll/admin_edit.html',
                  {'form': form,
                   'desgform':desgform,
                   'deptform':deptform,
                   'jobtypeform':jobtypeform
                   # 'salaryform':salaryform
                  })
                  
#this view adds a new employee
@login_required(login_url = "login")
@transaction.atomic
def add_employee(request):
    company=request.user.employee.company
    
    if request.method == "POST":
        
        userform = UserForm(request.POST)
        employeeform = EmployeeForm(request.POST)
        desgform=DesignationForm(request.POST)
        deptform=DepartmentForm(request.POST)
        jobtypeform=JobTypeForm(request.POST)
        
    
        print('deptform.is_valid()',deptform.is_valid())
        print('desgform.is_valid()',desgform.is_valid())
        print('jobtypeform.is_valid()',jobtypeform.is_valid())
        print('userform.is_valid()',userform.is_valid())
        print('employeeform.is_valid()',employeeform.is_valid())
        if  userform.is_valid() and employeeform.is_valid() and desgform.is_valid() and deptform.is_valid() and jobtypeform.is_valid() :
      
            
            user = userform.save(commit=False)
            user.is_active=False
            user.save()
            user.refresh_from_db()  # This will load the Employee created by the Signal
            employeeform = EmployeeForm(request.POST)
            print('employeeform',employeeform)
            employeeform.full_clean()
            
            
            employee_form=employeeform.save(commit=False)
            employee_form.is_admin = False
            employee_form.profile_pic = request.POST['profile_pic']
            employee_form.company = company
            employee_form.user = user
            employee_form.save()



            # current_site = get_current_site(request)
            # mail_subject = "Activate your Payroll account"
            # message = render_to_string("payroll/acc_active_email.html",{
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':account_activation_token.make_token(user),

            # })
            # print('token1')
            # to_email = employeeform.cleaned_data.get('emailid')
            # email = EmailMessage(mail_subject, message, to=[to_email]
            # )
            # email.send()

            
            #print('employee',employee)
            desgn=desgform.save(commit=False)
            desgn.date=datetime.datetime.now().date()
            desgn.employee=user.employee
            print(desgn.date)
            desgn.save()
            
            dept=deptform.save(commit=False)
            dept.date=datetime.datetime.now().date()
            dept.employee=user.employee
            dept.save()
            
            jobtype=jobtypeform.save(commit=False)
            jobtype.date=datetime.datetime.now().date()
            jobtype.employee=user.employee
            jobtype.save()
            
            
                     
            messages.success(request, ' New Employee Added Successful !')
            return redirect('add_employee')
        else:
            messages.success(request, 'Invalid Credentials !')
    else:
        userform = UserForm()
        employeeform = EmployeeForm()
        desgform=DesignationForm(company=company)
        deptform=DepartmentForm(company=company)
        jobtypeform=JobTypeForm(company=company)
        
    return render(request,
                  'payroll/add_employee.html',
                  {'userform':userform,
                   'employeeform':employeeform,
                   'desgform':desgform,
                   'deptform':deptform,
                   'jobtypeform':jobtypeform
                   
                   })
    

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print("user2",user)
    print("token2",token)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
                                
