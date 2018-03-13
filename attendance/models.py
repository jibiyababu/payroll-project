from django.db import models

class Attendance(models.Model):
    '''
    Attendance modules marks attendance per day for an employee
    '''
    employee=models.ForeignKey('user.Employee',blank=True,null=True)
    work_type=models.ForeignKey('company.Work_Type',blank=True, null=True)
    date=models.DateField(auto_now=True)
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
class Leave_Application(models.Model):
    '''
    Leave_Application models record leave application by employees
    '''
    employee=models.ForeignKey('user.Employee',blank=True,null=True)
    work_type=models.ForeignKey('company.Work_Type',blank=True, null=True)
    leave_from=models.DateField()
    leave_to=models.DateField()
    leave_type=models.CharField(max_length=200)
    def publish(self):
        self.save()
    def __str__(self):
        return self.employee+" "+str(self.leave_from)+"-"+str(self.leave_to)
