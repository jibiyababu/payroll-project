from django.db import models
from django.db.models import When, F, Q
from django.utils import timezone
from django.core.validators import RegexValidator

class Employee(models.Model):
    '''
    Employee model stores all the details of employee required for Payroll System
 
    '''
    name= models.CharField(max_length=50)
    address=models.TextField(max_length=100)
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in format :'+999999999'. ")
    contact=models.CharField(validators=[phone_regex],max_length=17)
    alter_Contact=models.CharField(validators=[phone_regex],max_length=17)
    emailid=models.EmailField()
    GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES,default="Select")
    Dob=models.DateField()
    #aadhar_regex=RegexValidator(regex=r'^\d{4}\s\d{4}\s\d{4}$',message="Invalid")
    #aadhar=models.IntegerField(validators=[aadhar_regex])
    #pan_regex='[a-zA-Z]{5}-[0-9]{4}-[a-zA-Z]{1}'
    profile_pic = models.ImageField(upload_to='payroll',default = 'None/no-img.jpg')
    tax_status_choices=(('NRI','NRI'),('RESIDENT','Resident'),('EXPAT','Expat'),)
    tax_status=models.CharField(default="None",max_length=8,choices=tax_status_choices,)
    privilegeleave=models.IntegerField(default=14)
    casualleave=models.IntegerField(default=10)
    joiningDate=models.DateField(blank=True,null=True)
    jobType=models.CharField(max_length=15,blank=True)
    jobLocation=models.CharField(max_length=15,blank=True)
    confirmationPeriod=models.IntegerField(blank=True,default=2)
    department=models.CharField(max_length=15,blank=True)
    salary=models.DecimalField(decimal_places=2,max_digits=10, default=decimal.Decimal('0.0000000000'))
    

    def publish(self):
        self.save()
    def __str__(self):
        return self.name

class Attendance(models.Model):
    '''
    Attendance modules marks attendance per day for an employee
    '''
    date=models.DateField()
    #ID_CHOICE=
    MARK_CHOICES=((1,'Present'),(0.5,'Halfday'),(0,'Absent'),(1,'WorkFromHome'))
    mark=models.IntegerField(choices=MARK_CHOICES)
    When(mark='Absent', then='leave_type')
    LEAVE_CHOICES=(('Privilege Leave','Privilege Leave'),('Casual Leave','Casual Leave'),)
    leave_type=models.CharField(max_length=15,choices=LEAVE_CHOICES)
    privilege_leave=models.BooleanField()
    casual_leave=models.BooleanField()

    def publish(self):
        self.save()
    #def __str__(self):
       # return self.
