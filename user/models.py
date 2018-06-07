import decimal
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.apps import apps
#mysalary = apps.get_model('payroll', 'Salary')



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
                                # primary_key=True,
                                null=True
                                )
    #name = models.CharField(max_length=200)
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
    emailid = models.EmailField()
    office_emailid = models.EmailField(null=True,blank=True)
    GENDER_CHOICES = (('M', 'Male'),
                      ('F', 'Female'),
                     )
    gender = models.CharField(max_length = 20,
                              choices = GENDER_CHOICES,
                              default = "Select"
                             )
    Dob = models.DateField(null=True)
    #aadhar_regex = RegexValidator(regex = r'^\d{4}\s\d{4}\s\d{4}$', message = "Invalid")
    #aadhar = models.IntegerField(validators=[aadhar_regex])
    #pan_regex = '[a-zA-Z]{5}-[0-9]{4}-[a-zA-Z]{1}'
    profile_pic = models.ImageField(upload_to = 'payroll',
                                    default = 'None/no-img.jpeg'
    )
    #tax_status_choices = (('NRI','NRI'), ('RESIDENT','Resident'), ('EXPAT','Expat'),)
    #tax_status = models.CharField(default = "None", max_length = 15, choices = tax_status_choices,)
    #privilegeleave = models.IntegerField(default = 14)
    #casualleave = models.IntegerField(default = 10)
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
                                           default = 2
                                          )
    #department = models.CharField(max_length = 50, blank = True)
    salary=models.DecimalField(max_digits = 10,
                               decimal_places = 3,
                               default = decimal.Decimal('0000000.000')
                              )
    is_admin = models.BooleanField(default=False)

    # @receiver(post_save, sender=User)
    # def update_employee(sender, instance, created, **kwargs):
    #     if created:
    #         Employee.objects.create(user=instance)
    #         instance.Employee.save()

        
    def __str__(self):
         return self.user.username


    
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
        return self.designation.designation

    
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
    #salary = models.ForeignKey("payroll.Salary",blank = True,null = True)
    
    date = models.DateField()
    # salary=models.DecimalField(max_digits = 10,
    #                            decimal_places = 3,
    #                            default = decimal.Decimal('0000000.000')
                               
    basic_percentage = models.FloatField(default = 35)
    hra_percentage = models.FloatField(default = 40)
    conveyance_allowance = models.IntegerField(default = 1600)
    special_allowance = models.IntegerField(default = 0)
    proffessional_tax = models.IntegerField(default = 200)
    income_tax = models.IntegerField(default = 0)
    # loss_of_pay = models.DecimalField(max_digits = 10,
    #                                   decimal_places = 7,
    #                                   default = decimal.Decimal('0000000.000')
    #                                  )
    # gross_earnings = models.DecimalField(max_digits = 10,
    #                                      decimal_places = 7,
    #                                      default = decimal.Decimal('0000000.000')
    #                                     )
    # gross_deductions = models.DecimalField(max_digits = 10,
    #                                        decimal_places = 7,
    #                                        default = decimal.Decimal('0000000.000')
    #                                       )
    # total_days = models.IntegerField(default = 00)
    # weekly_off = models.IntegerField(default = 00)
    # paid_days = models.IntegerField(default = 00)
    # net_salary = models.DecimalField(max_digits = 10,
    #                                  decimal_places = 7,
    #                                  default = decimal.Decimal('0000000.000'))

    def publish(self):
        self.save()

