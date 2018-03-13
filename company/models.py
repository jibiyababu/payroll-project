from django.db import models

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
    def publish(self):
        self.save()
    def __str__(self):
        return self.company.name+" "+self.work_type

class Designation(models.Model):
    '''
    designation model stores designations for particular company
    '''
    company=models.ForeignKey(Company, blank=True, null=True)
    designation=models.CharField(max_length=200)
    privilege_leave=models.IntegerField(default=0)
    casual_leave=models.IntegerField(default=0)
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

    
