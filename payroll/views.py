from .models import Salary
from user.models import Salary_History,Employee
from user.models import Department_History
from user.models import Designation_History
from user.models import Job_Type_History,Salary_Increment
from user.forms import SalaryIncrementForm
from attendance.models import Attendance
from company.models import Company
from company.models import Department,Holiday
from company.models import Designation,Work_Type
from company.views import add_worktype
from .forms import SalaryForm,SalaryReportForm
from .forms import Salary_History_Form
from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import calendar
from calendar import weekday, monthrange, SUNDAY ,SATURDAY
from num2words import num2words
from .render import *
from django.views.generic import View
import base64
import decimal
from payroll.decorators import work_type_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, time
import datetime
from threading import Thread, activeCount
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.template.loader import render_to_string


# view for updating salary-history of an employee

@login_required(login_url = "login")
def update_salary(request, pk = None):
    company=request.user.employee.company
    get_worktype(company)
    try:
        salary=Salary_Increment.objects.filter(employee=pk,effective_from__lte=timezone.now()).latest('id')
    except ObjectDoesNotExist:
        salary=None
    print('salary',salary)
        #if salary:
    if request.method=="POST":
        if salary:
            form=Salary_History_Form(request.POST)
            emp=request.POST['employee']
            print(form.is_valid())
            if form.is_valid():
                if not pk:
                    pk = request.POST['employee']
                record=form.save(commit=False)
            
                record.save()
                #messages.success(request,'Salary updated successfully')
                print('pk',pk)
                return redirect('salary_monthyear',pk=pk)
            else:
                messages.success(request,'Invalid Details !')
                return redirect('update_salary',pk=pk)
        else:
            messages.success(request,'Please add annual salary !')
            return redirect('update_salary',pk=pk)
            
    else:
        try:
            salary_history = Salary_History.objects.filter(employee_id=pk).latest('id')
            form=Salary_History_Form(company=company,instance=salary_history)
        except:
            
            salary_history={
                'employee':pk,
                'date':timezone.now()
            }
            #print('salary_history',salary_history.employee)
            form=Salary_History_Form(company=company,initial=salary_history)
    
        
        
    
    return render(request,
                  'payroll/update_salary_structure.html',
                  {'form':form}
    )


# function for calculation of basic of salary
def basic_sal(pk,basic_percentage):
    
    record=Salary_Increment.objects.filter(effective_from__lte=timezone.now()).latest('id')
    salary= float(record.salary)/12.0
    result=round((basic_percentage/100) * salary)
    return result

# function for calculation of hra of salary
def hra_sal(pk,hra_percentage):
    
    record=Salary_Increment.objects.filter(effective_from__lte=timezone.now()).latest('id')
    salary = float(record.salary)/12
    result = round((hra_percentage/100) * salary)
    return result

# function for calculation of Gross Earnings
def gross_earning(pk, basic, hra, conveyance_allow): # Function definition for gross_earning
    
    record=Salary_Increment.objects.filter(effective_from__lte=timezone.now()).latest('id')
    salary= float(record.salary)/12
    basic/=100
    basic_amount=basic * salary
    hra/=100
    hra_amount = hra * salary
    gross_earnings = basic_amount + hra_amount + conveyance_allow 
    print('type of gross earning',type(gross_earnings))
    print(gross_earnings)
    return gross_earnings

# function for calculation of Gross Deductions
def gross_deduction(pk, proffessional_tax, income_tax, lop): # Function definition for gross_deduction
    
    record=Employee.objects.get(pk=pk)
    gross_deductions = proffessional_tax + income_tax + lop
    return gross_deductions

    

# function for calculating weekends for a month depending on work-type of company
def check_weekend(company,saturday,sunday):
    try:
        worktype=Work_Type.objects.filter(company=company).latest('id')
        if worktype.worktype == 'SW':
            return sunday
        else:
            return saturday+sunday
        
    except:
        
        return 0
    

# function for calculating total present days of an employee for a month
def check_attendance(employee,month):
    try:
        attendance=Attendance.objects.filter(employee=employee,date__month=month,mark=1).annotate(Count('id'))
        
        return len(attendance)
    except:
        return None



# function for calculating loss of pay for an employee
def check_lossofpay(emp_pk,date):
    print('date',type(date))
    try:
        attendance=Attendance.objects.filter(employee=emp_pk, date__month=date.month, lop=True,mark=0).annotate(Count('id'))
        lop_days = len(attendance)
        
    except ObjectDoesNotExist:
        attendance=0
        lop_days = attendance

    employee = Salary_Increment.objects.filter(employee=emp_pk,effective_from__lte=date).latest('id')
    month_days = calendar.monthrange(date.year,date.month)[1] # returns month for eg: June, month=6
        
    salary_per_day = round((employee.salary/12)/month_days) # An Employee's annual salary is converted into salary per day 
    lop = lop_days * salary_per_day
    return lop


#this function checks worktype exist or not 
def get_worktype(company_id):
    try:
        worktype=Work_Type.objects.fiter(company=company_id)
    except:
        worktype = None
    if worktype:
        return redirect('update_salary')
    else:
        return redirect('add_worktype')
    



# This function returns department of an employee, if department exist else returns None
def get_department(employee):

    try:
        dept = Department_History.objects.filter(employee=employee).latest('id')    
        return dept

    except:
        dept = None
        return dept

# This function returns designation of an employee, if designaion exist else returns None
def get_designation(employee):

    try:
        desgn = Designation_History.objects.filter(employee = employee).latest('id')        
        return desgn

    except:
        desgn = None
        return desgn

# This function returns jobtype of an employee, if jobtype exist else returns None
def get_jobtype(employee):

    try:
        jobtype = Job_Type_History.objects.filter(employee = employee).latest('id')    
        return jobtype

    except:
        jobtype = None
        return jobtype

# This function returns salary object of an employee, if salary exist else returns None
def get_salary(employee):

    try:
        salary=Salary.objects.filter(employee=employee).latest('id')
        
        return salary
    except:
        salary=None
        return salary

@login_required(login_url = "login")
def salary_monthyear(request,pk=None):
    if request.method=="POST":
        form=SalaryForm(request.POST)
        monthyear=request.POST['month_year']
        date=datetime.datetime.strptime(str(monthyear), "%Y-%m-%d")
        try:
            salary=Salary_Increment.objects.filter(employee=pk,effective_from__lte=date).latest('id')
        except ObjectDoesNotExist:
            salary=None
        if salary:
            monthyear=request.POST['month_year']
            return redirect('salary_detail',pk=pk,monthyear=monthyear)
        else:
            messages.success(request,'Please add Annual Salary effective from month_year')
            return redirect('salary_monthyear',pk=pk)
    else:
        form=SalaryForm({'employee':pk})
    return render(request,'payroll/salary_monthyear.html',{'form':form,'pk':pk})
    
# This View calculates salary from salary-history of an employee
@login_required(login_url = "login")
def salary_detail(request,pk,monthyear):
    
    record=Employee.objects.get(pk=pk)
    salary_history = Salary_History.objects.filter(employee_id=pk).values().last()
    month_year=datetime.datetime.strptime(str(monthyear), "%Y-%m-%d")
    
    lop=check_lossofpay(pk,month_year) #  check_lossofpay() returns loss-of-pay for an employee
        
    data = {
        'month_year' : monthyear,
        'employee' : salary_history['employee_id'],
        'basic_percentage' : salary_history['basic_percentage'],
        'basic_amount' : basic_sal(salary_history['employee_id'],
                                   salary_history['basic_percentage']
        ) ,
        'hra_percentage' : salary_history['hra_percentage'],
        
        'hra_amount' : hra_sal(salary_history['employee_id'],
                               salary_history['hra_percentage']
        ) ,
        
        'conveyance_allowance' : salary_history['conveyance_allowance'],
        #'special_allowance' : salary_history['special_allowance'],
        
        'proffessional_tax' : salary_history['proffessional_tax'],
        'income_tax' : salary_history['income_tax'],
        'loss_of_pay':lop,
        # Function call for gross_earning
        'gross_earning' : gross_earning(salary_history['employee_id'],
                                        salary_history['basic_percentage'],
                                        salary_history['hra_percentage'],
                                        salary_history['conveyance_allowance']
                                        # salary_history['special_allowance']
        ) ,
        
        # Function call for gross_deduction
        'gross_deduction' : gross_deduction(salary_history['employee_id'],
                                            salary_history['proffessional_tax'],
                                            salary_history['income_tax'],
                                            lop                                         
        ) 
        
        
    }
    
    employee = Salary_Increment.objects.filter(effective_from__lte=timezone.now()).latest('id')
    salary_month = round((employee.salary/12))
    data['special_allowance'] =round(salary_month-( decimal.Decimal(data['gross_earning'])+data['gross_deduction']))
    data['gross_earning']+=float(data['special_allowance'])
    data['net_salary'] = decimal.Decimal(data['gross_earning']) - data['gross_deduction']
    data['bonus']=0
    # data['gross earning'] returns float hence it is converted to decimal
    
    if request.method=="POST" :
        form = SalaryForm(data,request.POST)
        
        print('form.bound:',form.is_bound)
        print('form.is_valid():',form.errors)
        #print('payslip_for_month',request.POST['payslip_for_month'])
        #monthyear=request.POST['month_year']
        
        # print('form',form.errors)
        # print('month-year',month,year)
        payslip = Salary.objects.filter(employee=pk,month_year=monthyear).exists()
        if form.is_valid():
            if not payslip:
                salary = form.save(commit=False)
                
                
                # print('month_year',month_year)
                now = datetime.datetime.now()
                month_days = calendar.monthrange(month_year.year, month_year.month)[1]
                print('month_days',month_days)
                matrix = calendar.monthcalendar(month_year.year,
                                                    month_year.month)
                x = sum(1 for x in matrix if x[SUNDAY] != 0)
                y = sum(1 for x in matrix if x[SATURDAY] != 0)
                holiday=Holiday.objects.filter(date__month=month_year.month).annotate(Count('id'))
                if holiday:
                    holiday=len(holiday)
                else:
                    holiday=0
                    
                start_date=date(month_year.year,month_year.month,1)
                end_date=date(month_year.year,month_year.month,month_days)
                count=Attendance.objects.filter(employee=pk,date__range=[start_date,end_date])
                weekend=check_weekend(request.user.employee.company,x,y)
                working_days=month_days-(weekend + holiday)
                print('holiday',holiday)
                print('weekend',weekend)
                print('len(count)',len(count))
                print('working_days',working_days)
                if len(count)==working_days:
                                         
                    
                    
                    salary.date= timezone.now()
                    salary.month_year=month_year
                        
                    salary.bonus = form.cleaned_data.get('bonus')
            
                    salary.total_days = month_days
                    salary.weekend = weekend # check_weekend() returns weekends based on company's wortype
                    
                
                    salary.public_holidays = holiday
                    salary.working_days = salary.total_days - (salary.weekend + salary.public_holidays)
                    salary.attendance = check_attendance(salary.employee,month_year.month)
                    
            
                    salary.save()
                    messages.success(request,'save successfully')
                    return redirect('salary_slip', pk=salary.pk)
                else:
                    messages.success(request,"Attendance for this month is not completed ")
                    return redirect('salary_detail',pk,monthyear)
            else:
                messages.success(request,"Payslip has already been generated for this month")
                return redirect('salary_detail',pk,monthyear)

        else:
            messages.success(request, 'Invalid Credentials.')
            return redirect('salary_detail',pk,monthyear)
                                         
    else:
        form=SalaryForm(data)

    return render(request,'payroll/salary_details.html',{'form':form,'pk':pk})

    



# def view_salary_slip(request):
                                         #     if request.method == 'POST':
                                         #         form = SalaryDateForm(request.POST)
                                         #         if form.is_valid():
                                         #             employee=form.cleaned_data_get('employee')
                                         #             start_date=form.cleaned_data_get('start_date')
                                         #             end_date=form.cleaned_data_get('end_date')
                                         #             record=Salary.objects.filter(employee=employee,month_year__range=[start_date,end_date])
             
#     return render(request,'payroll/view_salary_details.html',{'form':form,'pk':pk})




@login_required(login_url = "login")
def salary_increment(request):
    company=request.user.employee.company
    if request.method=="POST":
        form=SalaryIncrementForm(request.POST)
        if form.is_valid():
            record=form.save(commit=False)
            record.date=timezone.now()
            record.save()
            messages.success(request,"Salary incremented successfuly")
            return redirect('salary_increment')
        else:
            messages.success(request,"Invalid details")
            return redirect('salary_increment')
            
    else:
        form=SalaryIncrementForm(company=company)
    return render(request,'payroll/salary_increment.html',{'form':form})

@login_required(login_url = "login")
def salary_increment_list(request):
    company=request.user.employee.company
    if request.method=="POST":
        form=SalaryIncrementForm(request.POST)
        if form.is_valid():
            employee=request.POST['employee']
            record=Salary_Increment.objects.filter(employee=employee)
            return render(request,'payroll/salary_increment_list.html',{'form':form,'record':record})
        else:
            messages.success(request,"Invalid details")
            return redirect('salary_increment_list')
    else:
        form=SalaryIncrementForm(company=company)
    return render(request,'payroll/salary_increment_list.html',{'form':form})

        
#This view generates salary slip from salary of an employee
@login_required(login_url = "login")
def salary_slip(request,pk):
    

    salary = get_object_or_404(Salary,pk=pk)
    amount_words = num2words(salary.net_salary).title() #converts net_salary amount into words
    dept = get_department(salary.employee) 
    desgn = get_designation(salary.employee)
                                         
    return render(request,
                  'payroll/salary-slip-demo2.html',
                  {
                      'salary':salary,
                      'dept':dept,
                      'desgn':desgn,
                      'amount_words':amount_words
                  })

#this view renders html into pdf

@login_required(login_url = "login")
def report_salary_pdf(request,pk):
    salary = get_object_or_404(Salary,pk=pk)
    company = get_object_or_404(Company,pk=request.user.employee.company.pk)
    amount_words = num2words(salary.net_salary).title()
    dept = get_department(salary.employee)
    desgn = get_designation(salary.employee)
    logo=company.logo

    try:
        img_logo = open(logo.path,"rb")
        encoded_string = base64.b64encode(img_logo.read())
        
    except:
        encoded_string = logo
                                         
            
    params = {
        'salary':salary,
        'amount_words':amount_words,
        'dept':dept,
        'desgn':desgn,
        'encoded_string':encoded_string,
        'company':company,
        'request':request
    }
    return Render.render('payroll/sample_pdf2.html', params)

@login_required(login_url = "login")
def salary_pdf(request,pk):

    salary = get_object_or_404(Salary,pk=pk)
    company = get_object_or_404(Company,pk=request.user.employee.company.pk)
    amount_words = num2words(salary.net_salary).title()
    dept = get_department(salary.employee)
    desgn = get_designation(salary.employee)
                                         
    logo=company.logo

    try:
        img_logo = open(logo.path,"rb")
        encoded_string = base64.b64encode(img_logo.read())
        
    except:
        encoded_string = logo
                                         
            
    params = {
        'salary':salary,
        'amount_words':amount_words,
        'dept':dept,
        'desgn':desgn,
        'encoded_string':encoded_string,
        'company':company,
        'request':request
    }
    file = Render.render_to_file('payroll/sample_pdf2.html', params)
    
    print('file',file)
    mail_subject = "Payslip for %s"%(salary.month_year)
    
    message=''' Hello %s,

   Attached is payslip for %s from %s.


    Thanks & regards,
    %s,
    %s'''%(salary.employee.name,salary.month_year,company.name,request.user.employee.name,company.name)

    files=[("attachment", (file[0], open(file[1], "rb").read()))]
    message = EmailMessage(mail_subject, message,'support@mydomain.com',
                               [salary.employee.emailid,],)
                               
    attachment = open(file[1], 'rb')
    message.attach(file[0],attachment.read(),'application/pdf')
    message.send()
    return HttpResponse("Processed")
    


# @login_required(login_url = "login")
                                         # def salary_pending_list(request):

    
@login_required(login_url = "login")
def salary_pending_list(request):
    date_now = timezone.now().strftime("%Y-%m-%d")
    monthyear = datetime.datetime.strptime(date_now, "%Y-%m-%d").strftime("%m-%Y")
    message = None
    count=0
    emp_list=[]
    desgn_list = []
    dept_list = []
    jobtype_list = []
    salary_list = []
    salary_his_list = []
    company = request.user.employee.company.pk
    emp_count = Employee.objects.filter(company=company).annotate(Count('id'))
    
    #sal_count=Salary.objects.filter(month_year=monthyear)
                                         # print('salary for may',sal_count)
    for emp in emp_count:
        try:
            salary = Salary.objects.filter(employee = emp).latest('id')
            if not salary.month_year == monthyear:
                                         
                
                desgn = get_designation(emp)
                dept = get_department(emp)
                jobtype = get_jobtype(emp)
                salary = get_salary(emp)
                salary_his = Salary_History.objects.filter(employee= emp).latest('id')
                emp_list.append(emp)
                desgn_list.append(desgn)
                dept_list.append(dept)
                jobtype_list.append(jobtype)
                salary_list.append(salary)
                salary_his_list.append(salary_his)
            else:
                print(salary.employee,salary.date,salary.month_year)
                count+=1
        except ObjectDoesNotExist:
                                         

            # desgn = None
            # dept = None
            # jobtype = None
            # salary = None
            # salary_his =None
            
            desgn = get_designation(emp)
            dept = get_department(emp)
            jobtype = get_jobtype(emp)
            salary = None
            #salary_his = Salary_History.objects.filter(employee= emp).latest('id')
            salary_his=None
            emp_list.append(emp)
            desgn_list.append(desgn)
            dept_list.append(dept)
            jobtype_list.append(jobtype)
            salary_list.append(salary)
            salary_his_list.append(salary_his)
            #print('except:',emp_list)
    if not emp_list:
        message = "No pending salary to show"
        print(len(emp_count))
        print('count',count)
    paid=(count/len(emp_count))*100
    unpaid=((len(emp_count)-count)/len(emp_count))*100
    print('paid',paid)
    print('unpaid',unpaid)
    zipped_list=zip(emp_list,salary_list,dept_list, desgn_list, jobtype_list,salary_his_list)
    print(desgn_list)
    print(dept_list)
    print(jobtype_list)
    return render(request,'payroll/salary_pending_list.html',
                  {'zipped_list':zipped_list,
                   'date_now':timezone.now().strftime("%B-%Y"),
                   'message':message,
                   'paid':paid,
                   'unpaid':unpaid
                  })



                
@login_required(login_url = "login")
def salary_employee_list(request):
                                         
    desgn_list = []
    dept_list = []
    jobtype_list = []
    salary_list = []
    salary_his_list = []
    company = request.user.employee.company.pk
    date = timezone.now()
    #monthyear = datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime("%m-%Y")
    #salary_count = Salary.objects.exclude(month_year=monthyear)
    emp_count = Employee.objects.filter(company=company).annotate(Count('id'))
    #salary_count=salary.objects.latest('date')
    
    for emp in emp_count:

        desgn = get_designation(emp)
        dept = get_department(emp)
        jobtype = get_jobtype(emp)
        salary = get_salary(emp)
        try:
            salary_history = Salary_History.objects.filter(employee= emp).latest('id')
        except:
            salary_history = None
        desgn_list.append(desgn)
        dept_list.append(dept)
        jobtype_list.append(jobtype)
        salary_list.append(salary)
        salary_his_list.append(salary_history)
                                         
         # try:
         #     desgn=Designation_History.objects.filter(employee=c).latest('id')
         #     dept=Department_History.objects.filter(employee=c).latest('id')
         #     jobtype=Job_Type_History.objects.filter(employee=c).latest('id')
         #     salary=Salary.objects.filter(employee=c).latest('id')
         #     desgn_list.append(desgn)
         #     dept_list.append(dept)
         #     jobtype_list.append(jobtype)
         #     salary_list.append(salary)
         # except:
         #     desgn=None
         #     dept=None
         #     jobtype=None
         #     salary=None
         #     desgn_list.append(desgn)
         #     dept_list.append(dept)
         #     jobtype_list.append(jobtype)
         #     salary_list.append(salary)

    zipped_list=zip(emp_count, dept_list, desgn_list, jobtype_list, salary_list, salary_his_list)

    return render(request,'payroll/salary_employee_list.html',
                  {'zipped_list':zipped_list})

@login_required(login_url = "login")
def salary_report(request):
    company=request.user.employee.company
    if request.method=="POST":
                                         
        print('company',company)
        form=SalaryReportForm(request.POST)
        print(form)
        print(form.cleaned_data.get('employee'))
        if form.is_valid():
            emp_id=form.cleaned_data.get('employee')
            
            records=Salary.objects.filter(month_year__range=[request.POST['start_date'],request.POST['end_date']],employee=emp_id)
            print('records',records)
            messages.success(request,'Valid Credentials')
            return render(request,'payroll/salary_report.html',{'records':records})
        
        else:
            messages.success(request,'Invalid Details !')
            return redirect('view_salary')

    else:
        form=SalaryReportForm(company=company)

    return render(request,'payroll/salary_view.html',{# 'salary':salary,
        'form':form })
