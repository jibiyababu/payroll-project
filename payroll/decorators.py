from company.models import Designation
from company.models import Department
from company.models import Job_Type
from company.models import Work_Type
from company.views import add_worktype
from django.shortcuts import redirect
def work_type_required(function):
    def wrap(request, *args, **kwargs):
        try:
            worktype = Work_Type.objects.get(company=kwargs['company_id'])
        except:
            worktype=None
            
        if worktype == None:
            return function(request, *args, **kwargs)
        else:
            return redirect(add_worktype)
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
                                            
