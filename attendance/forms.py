from django import forms
from .models import Attendance
from .models import Leave_Application
from user.models import Employee
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.forms import formset_factory,BaseFormSet
class DateInput(forms.DateInput):
        input_type = 'date'


class AttendanceForm(forms.ModelForm):
   
        
        class Meta:
                model = Attendance
                fields = ('id',
                          'employee',
                          'mark',
                          'leave_type',          
                )
        
                widgets = {
                        'id':forms.Select(attrs={'class': 'form-control'}),
                        'employee':forms.Select(attrs={'class': 'form-control'}),

                        
                        'mark':forms.RadioSelect(attrs={'class': 'form-control','placeholder':'Company Name'}),
                        'leave_type':forms.Select(attrs={'class': 'form-control','placeholder':'Company Name'}),
             
                }

        def __init__(self,*args,**kwargs):
                company_id=kwargs.pop('company',False)
                #company_id=company
                super().__init__(*args,**kwargs)
                if company_id:
                        
                        self.fields['employee'] = forms.ModelChoiceField(queryset=Employee.objects.filter(company=company_id), widget=forms.Select(attrs={'class':'form-control'}))
           
class ViewAttendanceCompanyForm(forms.Form):
        
        monthdate= forms.DateField(  widget=DateInput(attrs={'class':'form-control'}))



class BaseAttendanceFormSet(BaseFormSet):
        def get_form_kwargs(self, index):
                kwargs = super().get_form_kwargs(index)
                kwargs['custom_kwarg'] = index
                return kwargs
                
class ViewAttendanceForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
                company_id = kwargs.pop('company','False')
                super(ViewAttendanceForm, self).__init__(*args, **kwargs)
                self.fields['start_date']=forms.DateField( widget=DateInput(attrs={'class':'form-control'}))
                self.fields['end_date']=forms.DateField(  widget=DateInput(attrs={'class':'form-control'}))
                
                self.fields['mark'].widget.attrs['class']='form-control'
                self.fields['employee'] = forms.ModelChoiceField(queryset=Employee.objects.filter(company=company_id), widget=forms.Select(attrs={'class':'form-control'}))

   
        class Meta:
                model= Attendance
                fields=('employee','mark')
                # fields = AttendanceForm.Meta.fields + ('start_date','end_date',)

                Widgets={ 
                          'employee':forms.Select(attrs={'class': 'form-control','placeholder':'Employee Name'}),
                        'mark':forms.Select(attrs={'class': 'form-control','placeholder':'Employee Name'})
                          
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
