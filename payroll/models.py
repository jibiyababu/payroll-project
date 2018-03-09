import decimal
import datetime
import calendar
from calendar import weekday, monthrange, SUNDAY ,SATURDAY
from django.db import models
from django.db.models import When, F, Q
from django.utils import timezone
from django.core.validators import RegexValidator

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
    tax_status_choices=(('NRI','NRI'),('RESIDENT','Resident'),('EXPAT','Expat'),)
    tax_status=models.CharField(default="None",max_length=15,choices=tax_status_choices,)
    privilegeleave=models.IntegerField(default=14)
    casualleave=models.IntegerField(default=10)
    joiningDate=models.DateField(blank=True,null=True)
    jobType=models.CharField(max_length=15,blank=True)
    jobLocation=models.CharField(max_length=50,blank=True)
    confirmationPeriod=models.IntegerField(blank=True,default=2)
    department=models.CharField(max_length=50,blank=True)
    salary=models.DecimalField(decimal_places=2,max_digits=10, default=decimal.Decimal('0.0000000000'))
    

    def publish(self):
        self.save()
    def __str__(self):
        return self.name

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
    isHalfDay=models.BooleanField()
    isWorkFromHome=models.BooleanField()
    #remPrivilegeLeave
    #remCasualLeave
    def publish(self):
        self.save()
    #def __str__(self):
       # return self.
class Salary(models.Model):
    '''
    Salary details accepts allowance and deductions details and calculates gross earnings and gross deductions
    '''
    employee=models.ForeignKey(Employee,related_name='+',blank=True,null=True)
    #salary=employee.salary
    #monthly_salary=salary/12
    date=models.DateField()

    basicPercentage=models.FloatField(default=35)
    #basic=(basicPercentage/float(100)) * monthly_salary/12

    hraPercentage=models.FloatField(default=40)
    #hra=(hraPercentage/float(100)) * monthly_salary/12

    conveyanceAllowance=models.IntegerField(default=1600)
    specialAllowance=models.IntegerField(default=0,blank=True)
    
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


    
    def publish(self):
        self.save()
    
