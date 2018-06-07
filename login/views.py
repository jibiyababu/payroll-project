from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login as user_login,logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm
from .forms import UserForm
from .forms import EmployeeForm
from company.forms import CompanyForm
from django.contrib.auth.models import User
from user.models import Employee
from company.views import company_homepage
from django.db import transaction
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
    return render (request,'login/homeindex.html')



@transaction.atomic
def admin_signup(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        employeeform = EmployeeForm(request.POST)
        companyform = CompanyForm(request.POST)
        if  userform.is_valid() and employeeform.is_valid() and companyform.is_valid() :
            
            company=companyform.save()
            company.refresh_from_db()
            user = userform.save(commit=False)
            user.is_staff=True
            user.save()
            user.refresh_from_db()  # This will load the Employee created by the Signal
            employeeform = EmployeeForm(request.POST)
            print('employeeform',employeeform)
            employeeform.full_clean()
            employee=employeeform.save(commit=False)
            employee.is_admin = True
            employee.company=company
            employee.user=user
            employee.save()
            messages.success(request, 'SignUp Successful !')
            return redirect(login)
    else:
        userform = UserForm()
        employeeform = EmployeeForm()
        companyform = CompanyForm()
    return render (request,'login/signup.html',{'companyform':companyform,
                                               'userform':userform ,
                                               'employeeform':employeeform
                                                
                                                }
                  )
        
def employee_detail(request):
    return render(request,'login/employee_detail.html')

def login(request):

    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                
                user_login(request,user)
                record=Employee.objects.get(user=user,is_admin=True)
                # if record:
                #     request.session['is_admin']=True
                #     request.session['company']=record.company
                
                messages.success(request, 'Admin Login Successful !')
                if user.is_staff and user.employee.is_admin:
                    return redirect('company_homepage')
                # else:
                #     messages.success(request, 'Employee Login Successful !')
                #     return redirect('employee_detail')
                    
            else:
                messages.success(request, 'Invalid Credentials.')
                return redirect('login')       
    return render(request,'login/login.html',{})

def logout_view(request):
    logout(request)
    messages.success(request,'Logout Successful !')
    return redirect('login')
