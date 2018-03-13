import decimal
import datetime
import calendar
from calendar import weekday, monthrange, SUNDAY ,SATURDAY
from django.db import models
from django.db.models import When, F, Q
from django.utils import timezone
from django.core.validators import RegexValidator    
class Salary(models.Model):
    '''
    Salary details accepts allowance and deductions details and calculates gross earnings and gross deductions
    '''
    employee=models.ForeignKey("user.Employee",related_name='+',blank=True,null=True)
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
    

