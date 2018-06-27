import decimal
import datetime
import calendar
from django.db import models
from django.db.models import When, F, Q
from django.utils import timezone
from django.core.validators import RegexValidator
from calendar import weekday, monthrange, SUNDAY ,SATURDAY


class Salary(models.Model):
    '''
    Salary details accepts allowance and deductions details and 
    calculates gross earnings, gross deeductions and net salary
    '''
    employee = models.ForeignKey("user.Employee",
                               related_name = '+',
                               blank = True,
                               null = True
                              )
    
    date = models.DateField()
    month_year = models.DateField(blank=True)
    basic_percentage = models.FloatField(default = 35)
    basic_amount=models.FloatField(default = 0)
    hra_amount=models.FloatField(default = 0)
    hra_percentage = models.FloatField(default = 40)
    conveyance_allowance = models.IntegerField(default = 1600)
    special_allowance = models.IntegerField(default = 0)
    bonus = models.IntegerField(default=0)
    proffessional_tax = models.IntegerField(default = 200)
    income_tax = models.IntegerField(default = 0)
    loss_of_pay = models.DecimalField(max_digits = 10,
                                      decimal_places = 3,
                                      default=decimal.Decimal('0000000.000')
                                 )
    gross_earning = models.DecimalField(max_digits = 10,
                                      decimal_places = 2,
                                      default = decimal.Decimal('0000000.000')
                                     )
    gross_deduction = models.DecimalField(max_digits = 6,
                                        decimal_places = 2,
                                        default = decimal.Decimal('0000.00')
                                       )
    
    total_days = models.IntegerField(default = 25)
    weekend = models.IntegerField(default = 8)
    public_holidays = models.IntegerField(default = 0)
    working_days=models.IntegerField(default = 22)
    attendance=models.IntegerField(null=True)
    net_salary=models.DecimalField(max_digits = 10,
                                   decimal_places = 3,
                                   default = decimal.Decimal('0000000.000')
                                  )
    
    
    def publish(self):
        
        self.save()
    def __str__(self):
         return self.employee.user.username



