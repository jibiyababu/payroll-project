import decimal
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Employee(models.Model):
    '''
    Employee model stores all the details of employee required for Payroll System
 
    '''
    company = models.ForeignKey('company.Company',
                                 null=True,
                                 blank=True
                                )
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True
                                )
    
    name = models.CharField(max_length = 50,null=True)
    address = models.TextField()
    phone_regex = RegexValidator(regex = r'^\+?1?\d{9,15}$',
                                 message = "Phone number must be entered in format :'+999999999'. "
                                )
    contact = models.CharField(validators = [phone_regex],
                               max_length = 17
                              )
    alter_Contact = models.CharField(validators = [phone_regex],
                                     max_length=17
                                    )
    emailid = models.EmailField(null=True)
    office_emailid = models.EmailField(null=True,blank=True)
    GENDER_CHOICES = (('M', 'Male'),
                      ('F', 'Female'),
                     )
    gender = models.CharField(max_length = 20,
                              choices = GENDER_CHOICES,
                              default = "Select"
                             )
    Dob = models.DateField(null=True)
    profile_pic = models.ImageField(upload_to = 'payroll',
                                    default = 'None/no-img.jpeg'
    )
    joining_date = models.DateField(blank = True,
                                    null = True
                                   )
    job_type = models.CharField(max_length = 15,
                                blank = True,
                                null=True
                               )
    job_location = models.CharField(max_length = 50,
                                    blank = True,
                                    null=True
                                   )
    probation_period = models.IntegerField(blank = True,
                                           null=True
                                          )
    is_admin = models.BooleanField(default=False)


        
    def __str__(self):
        return str(self.user)


    
class Designation_History(models.Model):
    '''
    Designation_History model  records designation_history for particular employee
    '''
    employee = models.ForeignKey(Employee,
                                 blank = True,
                                 null = True
                                )
    designation = models.ForeignKey('company.Designation',
                                  blank = True,
                                  null = True
                                 )
    date = models.DateField()
    
    def publish(self):
        self.save()
        
    def __str__(self):
        return self.designation.designation+" " +str(self.employee)

    
class Department_History(models.Model):
    '''
    Designation_History model  records designation_history for particular employee
    '''
    employee = models.ForeignKey(Employee,
                                 blank = True,
                                 null = True
                                )
    department = models.ForeignKey('company.Department',
                                 blank = True,
                                 null = True
                                )
    date = models.DateField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.department.department


    
class Job_Type_History(models.Model):
    '''
    Designation_History model  records designation_history for particular employee
    '''
    employee = models.ForeignKey(Employee,
                                 blank = True,
                                 null = True
                                )
    job_type = models.ForeignKey('company.Job_Type',
                                 blank = True,
                                 null = True
                                )
    date=models.DateField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.job_type.jobtype


class Leave_History(models.Model):
    
    '''
    Leave_History records total leaves taken by an employee
    '''
    employee = models.ForeignKey(Employee,
                                 blank = True,
                                 null = True
    )
    work_type = models.ForeignKey("company.Work_Type",
                                  blank = True,
                                  null = True
    )
    attendance = models.ForeignKey("attendance.Attendance",
                                   blank = True,
                                   null = True
    )
    leave_type = models.CharField(max_length = 200,
                                  default = "None"
    )
    date=models.DateField()
   
    def publish(self):
        self.save()
        
    def __str__(self):
        return self.employee.name+"Leave History"

    
class Salary_History(models.Model):
    '''
    Salary_History records Salary details of an employee
    '''
    employee = models.ForeignKey(Employee,
                                 related_name = '+',
                                 blank = True,
                                 null = True
                                )
    date = models.DateField()                           
    basic_percentage = models.FloatField(default = 35)
    hra_percentage = models.FloatField(default = 40)
    conveyance_allowance = models.IntegerField(default = 1600)
    proffessional_tax = models.IntegerField(default = 200)
    income_tax = models.IntegerField(default = 0)
    
    def publish(self):
        self.save()

class Salary_Increment(models.Model):
    '''
    Salary_Increment records salary-increment details of an employee
    '''
    date = models.DateField()
    employee = models.ForeignKey(Employee,
                                 related_name = '+',
                                 blank = True,
                                 null = True
                                )
    salary = models.DecimalField(max_digits = 10,
                               decimal_places = 3,
                                 default = decimal.Decimal('0000000.000'),
                                 blank=True
                              
                              )
    effective_from = models.DateField(blank=True)
    def publish(self):
        self.save()
        
    def __str__(self):
        return self.employee.user.username+" "+str(self.effective_from)
