from django import forms
from .models import Attendance
from .models import Leave_Application
from user.models import Employee
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.forms import formset_factory
class DateInput(forms.DateInput):
        input_type = 'date'


class AttendanceForm(forms.ModelForm):
   
        
        class Meta:
                model = Attendance
                fields = ('employee',
                   'mark',
                  'leave_type'
                  
        )
        
                widgets = {
            'employee':forms.Select(attrs={'class': 'form-control','placeholder':'Company Name'}),
            'work_type':forms.Select(attrs={'class': 'form-control','placeholder':'Company Name'}),
            'date':DateInput(attrs={'class': 'form-control','placeholder':'Company Name'}),
               
            'mark':forms.RadioSelect(attrs={'class': 'form-control','placeholder':'Company Name'}),
            'leave_type':forms.Select(attrs={'class': 'form-control','placeholder':'Company Name'}),
             
                }

        def __init__(self, *args, **kwargs):
                company_id=kwargs.pop('company',False)
                super(AttendanceForm, self).__init__(*args, **kwargs)
        

                if company_id:
                        # emp_count=Employee.objects.filter(company=company_id)
                        
                        # for emp in emp_count:
                        #         try:
                        #                 record=Attendance.objects.filter(employee=emp).latest('id')
                        #                 if not record.date == timezone.now():
                        #                         l.append(emp)
                        #         except ObjectDoesNotExist:
                        #                 l.append(emp)
                        #                 print('emp_count:',emp_count)                
                        # print('emp_list:',l)
                        
                        self.fields['employee'] = forms.ModelChoiceField(queryset=Employee.objects.filter(company=company_id), widget=forms.Select(attrs={'class':'form-control'}))
        ##}}
                                                                          # 
        #                                                                  
class ViewAttendanceCompanyForm(forms.Form):
        monthdate=forms.DateField(  widget=DateInput(attrs={'class':'form-control'}))
                
class ViewAttendanceForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
                # company_id = kwargs.pop('company_id','')
                super(ViewAttendanceForm, self).__init__(*args, **kwargs)
                self.fields['start_date']=forms.DateField( widget=DateInput(attrs={'class':'form-control'}))
                self.fields['end_date']=forms.DateField(  widget=DateInput(attrs={'class':'form-control'}))
                self.fields['employee'].widget.attrs['class']='form-control'

   
        class Meta:
                model= Attendance
                fields=('employee',)
                # fields = AttendanceForm.Meta.fields + ('start_date','end_date',)

                Widgets={ 
                          'employee':forms.Select(attrs={'class': 'form-control','placeholder':'Employee Name'})
                          
                   }        

class LeaveApplicationForm(forms.ModelForm):
        class Meta:
                model= Leave_Application
                fields=('employee','leave_from','leave_to','leave_type','remark')
                widgets = {
            'employee':forms.Select(attrs={'class': 'form-control','placeholder':'Company Name'}),
            'leave_type':forms.Select(attrs={'class': 'form-control','placeholder':'Company Name'}),
            'leave_from':DateInput(attrs={'class': 'form-control','placeholder':'Company Name'}),
             'leave_to':DateInput(attrs={'class': 'form-control','placeholder':'Company Name'}),
              'remark':forms.Select(attrs={'class': 'form-control','placeholder':'Remark'})
                        }
