from django import forms
from .models import Salary
from user.models import Employee
from user.models import Salary_History
import datetime

class DateInput(forms.DateInput):
        input_type = 'date'


class SalaryDateForm(forms.ModelForm):
        start_date = forms.DateInput(attrs={'class':'form-control','placeholder':'Date','type':'date'})
        end_date = forms.DateInput(attrs={'class':'form-control','placeholder':'Date','type':'date'})
        class Meta:
                model=Salary
                fields=('employee',)
                # widgets={
                #         'employee':forms.select(attrs={'class': 'form-control','placeholder':'Employee','disabled':'disabled'}))
                # }
        def __init__(self, *args, **kwargs):
                company_id=kwargs.pop('company',False)
                super(SalaryDateForm, self).__init__(*args, **kwargs)
                self.fields['employee'] = forms.ModelChoiceField(queryset=Employee.objects.filter(company=company_id), widget=forms.Select(attrs={'class':'form-control'}))
                
class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        fields = ('employee', 'basic_percentage','basic_amount','hra_amount', 'hra_percentage', 'conveyance_allowance', 'special_allowance', 'proffessional_tax', 'income_tax', 'loss_of_pay', 'gross_earning', 'gross_deduction', 'net_salary','month_year')
        
       
        widgets = {
                # 'date': DateInput(attrs={'class':'form-control','placeholder':'Date','disabled':'disabled'}),
                'employee': forms.Select(attrs={'class': 'form-control','placeholder':'Employee','disabled':'disabled'}),
                'basic_percentage':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Basic','disabled':'disabled'}),
                'hra_percentage': forms.NumberInput(attrs={'class': 'form-control','placeholder':'HRA','disabled':'disabled'}),
                'conveyance_allowance': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Conveyance Allowance','disabled':'disabled'}),
                'special_allowance': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Special Allowance','disabled':'disabled'}),
                'proffessional_tax': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Proffesional Tax','disabled':'disabled'}),
                'income_tax': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Income Tax','disabled':'disabled'}),
                'loss_of_pay': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Loss of Pay','disabled':'disabled'}),
                'gross_earning': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Gross Earning','disabled':'disabled'}),
                'gross_deduction': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Gross Deduction','disabled':'disabled'}),
                'net_salary': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Net Salary','disabled':'disabled'}),
                'basic_amount': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'basic','disabled':'disabled'}),
                'hra_amount': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'hra','disabled':'disabled'}),
                'month_year':forms.DateInput(attrs={'class':'form-control','placeholder':'Date','type':'date'}),
                
        }

    def clean_month_year(self):
            date = self.cleaned_data['month_year']
            if date > datetime.date.today():
                    
                    raise forms.ValidationError("The date cannot be in the future!")
                    #self.add_error('date',msg)
            return date


        
        # def __init__(self, *args, **kwargs):
        #     super(SalaryForm, self).__init__(*args, **kwargs)
        #     for field in self.fields():
        #         field.widget.attrs['class'] = 'form-control'
             
class Salary_History_Form(forms.ModelForm):
        
        class Meta:
                model = Salary_History
                fields=('employee','date','basic_percentage','hra_percentage','conveyance_allowance','special_allowance','proffessional_tax','income_tax')
                
                widgets = {
                        'date': DateInput(attrs={'class':'form-control','placeholder':'Date'}),
                        'employee': forms.Select(attrs={'class': 'form-control','placeholder':'Employee'}),
                        'basic_percentage':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Basic'}),
                        'hra_percentage': forms.NumberInput(attrs={'class': 'form-control','placeholder':'HRA'}),
                        'conveyance_allowance': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Conveyance Allowance'}),
                        'special_allowance': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Special Allowance'}),
                        'proffessional_tax': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Proffesional Tax'}),
                        'income_tax': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Income Tax'})
                        

                  }
                
                    
        def clean(self):
                self.employee = self.cleaned_data['employee']
                print(self.employee)        
                
# class EmployeeForm(forms.ModelForm):
#         class Meta:
#                 model = Employee
#                 fields=('salary',)
#                 widgets = {
#                           'salary': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Net Salary'})
#                 }
class SalaryReportForm(forms.ModelForm):

        start_date=forms.DateField(widget=DateInput(attrs={'class':'form-control'}))
        end_date=forms.DateField( widget=DateInput(attrs={'class':'form-control'}))
        def __init__(self, *args, **kwargs):
                company_id=kwargs.pop('company',False)
                super(SalaryReportForm, self).__init__(*args, **kwargs)
                if company_id:
                        self.fields['employee'] = forms.ModelChoiceField(queryset=Employee.objects.filter(company=company_id), widget=forms.Select(attrs={'class':'form-control'}))
  
        class Meta:
                model= Salary
                fields=('employee',)
                widgets = {
                        'employee': forms.Select(attrs={'class': 'form-control','placeholder':'Employee'})
                }
