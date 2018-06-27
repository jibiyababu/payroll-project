from django.db import models

class Company(models.Model):
    '''
    Company model stores details of company
    '''
    name = models.CharField(max_length = 250,unique=True)
    logo = models.ImageField(upload_to = 'payroll',
                                    default = 'None/payroll_logo.png'
                             )
    address_line_1 = models.CharField(max_length = 200)
    address_line_2 = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    postal_code = models.IntegerField(default = 0000)
    country = models.CharField(max_length = 200)
    fax = models.CharField(max_length = 17)
    website = models.CharField(max_length = 200,unique=True)

    def publish(self):
        self.save()
        
    def __str__(self):
        return self.name

    
class Holiday(models.Model):
    '''
    Holiday models stores date for all holiday falling in a year
    '''
    company = models.ForeignKey(Company, blank=True, null=True)    
    date = models.DateField()
    NAME_CHOICES = (('RD','Republic Day'),
                    ('MSHIV','Maha Shivaratri'),
                    ('HOLI','Holi'),
                    ('RM','Rama Navami'),
                    ('MJ','Mahavir Jayanti'),
                    ('GF','Good Friday'),
                    ('BP','Buddha Purnima'),
                    ('IDF',"Idu'l Fitr"),
                    ('ID','Independence Day'),
                    ('IDZ','Id-ul-Zuha(Bakrid)'),
                    ('JN','Janmashtarni (Vaishnav)'),
                    ('GC','Ganesh Chaturthi/Vinayaka Chaturthi'),
                    ('MUH','Muharram/Ashura'),
                    ('MGJ','Mahatma Gandhi Jayanti'),
                    ('DUS','Dussehra'),
                    ('DIW','Diwali (Deepavali)'),
                    ('ID','Id-e- Milad (birthday of Prophet Mohammad)'),
                    ('GN',"Guru Nanak's Birthday"),
                    ('CD','Christmas Day'),
                    ('Nd','New Year Day'),
                    ('MSANK','Makar Sankranti')
    )
    name = models.CharField(max_length=200,choices=NAME_CHOICES)

    def publish(self):
        self.save()
        
    def __str__(self):
        return self.name

    
class Work_Type(models.Model):
    '''
    Work_Type model customises the work structure for particular company
    '''
    company = models.ForeignKey(Company, blank = True, null = True)
    WORK_TYPE_CHOICES = (('SH','Saturday Halfday'),
                         ('SW','Saturday Working'),
                         ('SSH','Saturday-Sunday Holiday')
                        )
    worktype = models.CharField(max_length = 200,choices=WORK_TYPE_CHOICES)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.worktype

    
class Designation(models.Model):
    '''
    designation model stores designations for particular company
    '''
    company = models.ForeignKey(Company,
                                blank = True,
                                null = True
                               )
    
    DESIGNATION_CHOICES = (('CTO','Chief Technology Officer'),
                           ('CMO','Chief Marketing Officer'),
                           ('CAO','Chief Accounting Officer'),
                           ('CLO','Chief Legal Officer'),
                           ('CEO','Chief Executive Manager'),
                           ('SD','Senior Developer'),
                           ('JD','Junior Developer'),
                           ('HRM','Human Resource Manager'),
                           ('INT','INTERN'),
                          
                          )
    designation = models.CharField(max_length = 200,choices=DESIGNATION_CHOICES)
    privilege_leave = models.IntegerField(default = 0)
    casual_leave = models.IntegerField(default = 0)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.designation


class Department(models.Model):
    '''
    department model stores department details for particular company
    '''
    company = models.ForeignKey(Company,
                                blank=True,
                                null=True
                               )
    DEPARTMENT_CHOICES = (('PROD','Production'),
                          ('DEV','Development'),
                          ('RND','Research and Development'),
                          ('HRM','Human Resource Management'),
                          ('MRK','Marketing'),
                          ('ANF','Accounting and Finance' )
                          

                         )
    department = models.CharField(max_length = 200, choices=DEPARTMENT_CHOICES)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.department

    
class Job_Type(models.Model):
    '''
    Job_Type model stores job_type details applicable for particular company
    '''
    company = models.ForeignKey(Company,
                                blank = True,
                                null = True)
    JOB_TYPE_CHOICES = (('PROB','Probation'),
                        ('PER','Permanent Employee'),
                        ('TEM','Temporary Employee')
                       )
    jobtype = models.CharField(max_length=200, choices=JOB_TYPE_CHOICES, default='PE')

    def publish(self):
        self.save()

    def __str__(self):
        return self.jobtype

    
