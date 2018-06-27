from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login as user_login,logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from payroll.models import Salary
from company.models import Designation
from .forms import LoginForm
from user.forms import UserForm
from  user.forms import EmployeeForm
from company.forms import CompanyForm
from django.contrib.auth.models import User
from user.models import Employee, Designation_History
from company.views import company_homepage
from django.db import transaction
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import datetime
import calendar
from django.db.models import Sum
# Create your views here.


@login_required(login_url = "login")
def index(request):
    return render(request,'login/home.html')
@login_required(login_url = "login")
def dashboard(request):

    now = datetime.datetime.now().date()
    l=[]
    l.append(0)
    for i in range(1,13):
        start_date = datetime.datetime.strptime(str(now.year)+str(i),"%Y%m")
        end_date = datetime.datetime.strptime(
            str(start_date.year)+str(i)+str(calendar.monthrange(start_date.year,start_date.month)[1]),
            "%Y%m%d"
        )
        total = Salary.objects.filter(date__gte=start_date,date__lte=end_date).aggregate(Sum('net_salary'))
        if total['net_salary__sum']==None:
            l.append(0)
        else:
            l.append(int(total['net_salary__sum']))

    #try for pie chart :)
    d = list(Designation.objects.filter(company_id=request.user.employee.company_id).values('designation'))
    l2=[]
    for i in d:
        l2.append(i['designation'])

    empdictlist = list(Employee.objects.filter(company_id=request.user.employee.company_id).values('id'))
    employees=[]
    for i in empdictlist:
        employees.append(i['id'])
    
    l3=[]
    for i in l2:
        temp=0
        for j in employees:
            latest_des_id = Designation_History.objects.filter(employee_id=j).latest('id').designation_id
            des = list(Designation.objects.filter(id=latest_des_id).values('designation'))
            des = des[0]['designation']
            if i == des:
                temp+=1
        l3.append(temp)
                


    #todays birthday try :)
    birthday_emp = Employee.objects.filter(company_id=request.user.employee.company_id,Dob__month=now.month,Dob__day=now.day)
    # for emp in birthday_emp:
    #     user_id = emp.user_id
    #     mail_address = get_object_or_404(User, id=user_id).email 
    #     print("emp : ",emp,"   user_id : ",user_id,"  email : ",mail_address)


    #male female ratio
    males = Employee.objects.filter(company_id=request.user.employee.company_id,gender="M").count()
    females = Employee.objects.filter(company_id=request.user.employee.company_id,gender="F").count()
    
    return render(request,'login/dashboard.html',
                  {
                      "a1":l[1],
                      "a2":l[2],
                      "a3":l[3],
                      "a4":l[4],
                      "a5":l[5],
                      "a6":l[6],
                      "a7":l[7],
                      "a8":l[8],
                      "a9":l[9],
                      "a10":l[10],
                      "a11":l[11],
                      "a12":l[12],
                      "l2":l2,
                      "l3":l3,
                      "birthday_emp":birthday_emp,
                      "males":males,
                      "females":females,
                  }
    )





@transaction.atomic
def admin_signup(request):
    if request.user.is_authenticated:
        return redirect('company_homepage')
    else:
        if request.method == "POST":
            userform = UserForm(request.POST)
            employeeform = EmployeeForm(request.POST,request.FILES)
            companyform = CompanyForm(request.POST,request.FILES)
            print('companyform',companyform.errors)
            print('userform',userform.errors)
            print('employeeform',employeeform.errors)
            if  userform.is_valid() and employeeform.is_valid() and companyform.is_valid() :
                
                company=companyform.save(commit=False)
                company.logo = request.FILES['logo']
                company.save()
                company.refresh_from_db()
                user = userform.save(commit=False)
                user.is_staff=True
                user.save()
                user.refresh_from_db()  # This will load the Employee created by the Signal
                employeeform = EmployeeForm(request.POST)
                #print('employeeform',employeeform)
                employeeform.full_clean()
                employee=employeeform.save(commit=False)
                employee.profile_pic = request.FILES['profile_pic']
                employee.is_admin = True
                employee.company=company
                employee.user=user
                employee.save()
                messages.success(request, 'SignUp Successful !')
                return redirect(login)
        else:
            userform = UserForm()
            employeeform = EmployeeForm(prefix='employee')
            companyform = CompanyForm(prefix='company')
        return render (request,'login/signup.html',{'companyform':companyform,
                                               'userform':userform ,
                                               'employeeform':employeeform
                                                
                                                }
                  )
        
def employee_detail(request):
    return render(request,'login/employee_detail.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
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
                else:
                    messages.success(request, 'Incorrect Username or Password!')
                        
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
    return redirect('index')
