import decimal
import datetime
import calendar
from calendar import weekday, monthrange, SUNDAY ,SATURDAY
from django.db import models
from django.db.models import When, F, Q
from django.utils import timezone
from django.core.validators import RegexValidator

class Company(models.Model):
    '''
    Company model stores details of company
    '''
    name=models.CharField(max_length=250)
    address_line_1=models.CharField(max_length=200)
    address_line_2=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    postal_code=models.IntegerField(default=0000)
    country=models.CharField(max_length=200)
    fax=models.CharField(max_length=17)
    website=models.CharField(max_length=200)

    def publish(self):
        self.save()
    def __str__(self):
        return self.name

    
class Holiday(models.Model):
    '''
    Holiday models stores date for all holiday falling in a year
    '''
    company=models.ForeignKey(Company, blank=True, null=True)
    date=models.DateField()
    name=models.CharField(max_length=200)

    def publish(self):
        self.save()
    def __str__(self):
        return self.name

class Work_Type(models.Model):
    '''
    Work_Type model customises the work structure for particular company
    '''
    company=models.ForeignKey(Company, blank=True, null=True)
    work_type=models.CharField(max_length=200)
    
class Designation(models.Model):
    '''
    designation model stores designations for particular company
    '''
    company=models.ForeignKey(Company, blank=True, null=True)
    designation=models.CharField(max_length=200)
    privilege_leave=models.IntegerField(default=0)
    casual_leave=models.IntegerField(default=0)
    salary=models.DecimalField(decimal_places=7,max_digits=10, default=decimal.Decimal('0000000.000'))
    def publish(self):
        self.save()
    def __str__(self):
        return self.designation


class Department(models.Model):
    '''
    department model stores department details for particular company
    '''
    company=models.ForeignKey(Company, blank=True, null=True)
    department=models.CharField(max_length=200)
    
    def publish(self):
        self.save()
    def __str__(self):
        return self.department

    
class Job_Type(models.Model):
    '''
    Job_Type model stores job_type details applicable for particular company
    '''
    company=models.ForeignKey(Company, blank=True, null=True)
    job_type=models.CharField(max_length=200)

    def publish(self):
        self.save()
    def __str__(self):
        return self.job_type

    
class Employee(models.Model):
    '''
    Employee model stores all the details of employee required for Payroll System
 
    '''
    name= models.CharField(max_length=255)
    address=models.TextField()
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in format :'+999999999'. ")
    contact=models.CharField(validators=[phone_regex],max_length=17)
    alter_Contact=models.CharField(validators=[phone_regex],max_length=17)
    emailid=models.EmailField()
    GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
    gender=models.CharField(max_length=20,choices=GENDER_CHOICES,default="Select")
    Dob=models.DateField()
    #aadhar_regex=RegexValidator(regex=r'^\d{4}\s\d{4}\s\d{4}$',message="Invalid")
    #aadhar=models.IntegerField(validators=[aadhar_regex])
    #pan_regex='[a-zA-Z]{5}-[0-9]{4}-[a-zA-Z]{1}'
    profile_pic = models.ImageField(upload_to='payroll',default = 'None/no-img.jpeg')
    #tax_status_choices=(('NRI','NRI'),('RESIDENT','Resident'),('EXPAT','Expat'),)
    #tax_status=models.CharField(default="None",max_length=15,choices=tax_status_choices,)
    #privilegeleave=models.IntegerField(default=14)
    #casualleave=models.IntegerField(default=10)
    joining_date=models.DateField(blank=True,null=True)
    job_type=models.CharField(max_length=15,blank=True)
    job_location=models.CharField(max_length=50,blank=True)
    probation_period=models.IntegerField(blank=True,default=2)
    #department=models.CharField(max_length=50,blank=True)
    
    def publish(self):
        self.save()
    def __str__(self):
        return self.name

class Designation_History(models.Model):
    '''
    Designation_History model  records designation_history for particular employee
    '''
    employee=models.ForeignKey(Employee,blank=True, null=True)
    designation=models.ForeignKey(Designation, blank=True, null=True)
    date=models.DateField()
    def publish(self):
        self.save()
    def __str__(self):
        return self.designation.designation
    
class Department_History(models.Model):
    '''
    Designation_History model  records designation_history for particular employee
    '''
    employee=models.ForeignKey(Employee,blank=True, null=True)
    department=models.ForeignKey(Department, blank=True, null=True)
    date=models.DateField()
    def publish(self):
        self.save()
    def __str__(self):
        return self.department.department

class Job_Type_History(models.Model):
    '''
    Designation_History model  records designation_history for particular employee
    '''
    employee=models.ForeignKey(Employee,blank=True, null=True)
    job_type=models.ForeignKey(Job_Type, blank=True, null=True)
    date=models.DateField()
    def publish(self):
        self.save()
    def __str__(self):
        return self.job_type.job_type


    
class Attendance(models.Model):
    '''
    Attendance modules marks attendance per day for an employee
    '''
    employee=models.ForeignKey(Employee,blank=True,null=True)
    date=models.DateField()
    MARK_CHOICES=((1,'Present'),(0.5,'Halfday'),(0,'Absent'),)
    mark=models.IntegerField(choices=MARK_CHOICES,blank=True)
    LEAVE_CHOICES=(('Privilege Leave','Privilege Leave'),('Casual Leave','Casual Leave'),)
    leave_type=models.CharField(max_length=15,choices=LEAVE_CHOICES)
    #isHalfDay=models.BooleanField()
    #isWorkFromHome=models.BooleanField()
    #remPrivilegeLeave
    #remCasualLeave
    def publish(self):
        self.save()
    def __str__(self):
       return self.employee.name+" "+ str(self.date)

class Leave_History(models.Model):
    
    '''
    Leave_History records total leaves taken by an employee
    '''
    employee=models.ForeignKey(Employee,blank=True, null=True)
    attendance=models.ForeignKey(Attendance, blank=True, null=True)
    privilege_leave=models.IntegerField(default=0)
    casual_leave=models.IntegerField(default=0)
    date=models.DateField()
    def publish(self):
        self.save()
    def __str__(self):
        return self.employee.name+"Leave History"


   
    
    
class Salary(models.Model):
    '''
    Salary details accepts allowance and deductions details and calculates gross earnings and gross deductions
    '''
    employee=models.ForeignKey(Employee,related_name='+',blank=True,null=True)
    #salary=self.employee.salary
    #monthly_salary=salary/12
    date=models.DateField()

    basicPercentage=models.FloatField(default=35)
    #basic=(basicPercentage/float(100)) * monthly_salary/12

    hraPercentage=models.FloatField(default=40)
    #hra=(hraPercentage/float(100)) * monthly_salary/12

    conveyanceAllowance=models.IntegerField(default=1600)
    specialAllowance=models.IntegerField(default=0)
    
    proffesionalTax=models.IntegerField(default=200)
    incomeTax=models.IntegerField(default=0)
    lossOfPay=models.DecimalField(max_digits=5,decimal_places=2,default=decimal.Decimal('0.00000'))
    
    #gEarnings=basic+hra+conveyanceAllowance+specialAllowance
    grossEarnings=models.DecimalField(max_digits=5,decimal_places=2,default=decimal.Decimal('0.00000'))

    #gDeductions=proffesionalTax+incomeTax+lossOfPay
    grossDeductions=models.DecimalField(max_digits=5,decimal_places=2,default=decimal.Decimal('0.00000'))

    now=datetime.datetime.now()
    month_days=calendar.monthrange(now.year,now.month)[1]
    
    totalDays=models.IntegerField(default=month_days)

    matrix = calendar.monthcalendar(now.year,now.month)
    noOfSundays=sum(1 for x in matrix if x[SUNDAY] != 0)
    noOfSaturdays=sum(1 for x in matrix if x[SATURDAY] != 0)
    weekends=noOfSaturdays+noOfSaturdays
    weeklyoff=models.IntegerField(default=weekends)
    
    #publicHolidays=models.IntegerField(default=0)
    #paiddays=totalDays-(weeklyoff+publicHolidays)
    paidDays=models.IntegerField(default=22)
    net_salary=models.DecimalField(max_digits=10,decimal_places=7,default=decimal.Decimal('0000000.000'))
    
    
    def publish(self):
        self.save()
    
class Salary_History(models.Model):
    '''
    Salary_History records Salary details of an employee
    '''
    employee=models.ForeignKey(Employee,related_name='+',blank=True,null=True)
    salary=models.ForeignKey(Salary,blank=True,null=True)
    
    date=models.DateField()
    basic_percentage=models.FloatField(default=35)
    hra_percentage=models.FloatField(default=40)
    conveyance_allowance=models.IntegerField(default=1600)
    special_allowance=models.IntegerField(default=0)
    
    proffesional_tax=models.IntegerField(default=200)
    income_tax=models.IntegerField(default=0)
    loss_of_pay=models.DecimalField(max_digits=10,decimal_places=7,default=decimal.Decimal('0000000.000'))

    gross_earnings=models.DecimalField(max_digits=10,decimal_places=7,default=decimal.Decimal('0000000.000'))
    gross_deductions=models.DecimalField(max_digits=10,decimal_places=7,default=decimal.Decimal('0000000.000'))

    total_days=models.IntegerField(default=00)
    weekly_off=models.IntegerField(default=00)
    paid_days=models.IntegerField(default=00)
    net_salary=models.DecimalField(max_digits=10,decimal_places=7,default=decimal.Decimal('0000000.000'))

    def publish(self):
        self.save()
