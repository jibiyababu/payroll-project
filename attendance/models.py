from django.db import models


class Attendance(models.Model):
    '''
    Attendance modules marks attendance per day for an employee
    '''
    employee = models.ForeignKey('user.Employee',
                                 blank = True,
                                 null = True
                                )
    work_type = models.ForeignKey('company.Work_Type',
                                   blank = True,
                                   null = True
                                 )
    date = models.DateField()
    MARK_CHOICES = ((1,'Present'),
                  (0.5,'Halfday'),
                  (0,'Absent'),
                 )
    mark = models.IntegerField(choices = MARK_CHOICES,
                               blank=False,default=1
                              )
    LEAVE_CHOICES = (('Privilege Leave','Privilege Leave'),
                   ('Casual Leave','Casual Leave'),
                  )
    leave_type = models.CharField(max_length = 15,
                                  choices = LEAVE_CHOICES,
                                  blank = True
                               )
    remPrivilegeLeave=models.IntegerField(null=True,blank=True)
    remCasualLeave=models.IntegerField(null=True,blank=True)
    pl=models.IntegerField(default=0)
    cl=models.IntegerField(default=0)
    lop=models.BooleanField(default=False)
    def publish(self):
        self.save()

    def __str__(self):
        return str(self.employee.user.username)+str(self.date) + " " + str(self.mark)
 

class Leave_Application(models.Model):
    '''
    Leave_Application models record leave application by employees
    '''
    employee = models.ForeignKey('user.Employee',
                                  blank = True,
                                  null = True
                                 )
    work_type = models.ForeignKey('company.Work_Type',
                                  blank = True,
                                  null = True
                                 )
    leave_from = models.DateField()
    leave_to = models.DateField()
    LEAVE_CHOICES = (('Privilege Leave','Privilege Leave'),
                   ('Casual Leave','Casual Leave'),
                  )
    leave_type = models.CharField(max_length = 200,choices=LEAVE_CHOICES)
    
    REMARK_CHOICES=(('S','Sanctioned'),('NS','Not Sanctioned'))
    remark=models.CharField(max_length = 200,choices=REMARK_CHOICES,blank=True, null=True)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.employee.user.username + " " + str(self.leave_from) + "-" + str(self.leave_to)
