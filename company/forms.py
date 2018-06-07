from django import forms
from .models import Company
from .models import Holiday
from .models import Work_Type
from .models import Department
from .models import Designation
from .models import Job_Type
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# class SignUpForm(UserCreationForm):

    
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', )
#     def __init__(self, *args, **kwargs):
#         company_id = kwargs.pop('company_id','')
#         super(SignUpForm, self).__init__(*args, **kwargs)
#         self.fields['company']=forms.ModelChoiceField(queryset=Company.objects.filter(company=company_id))

class DateInput(forms.DateInput):
        input_type = 'date'

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name',
                  'address_line_1',
                  'address_line_2',
                  'state',
                  'postal_code',
                  'country',
                  'fax',
                  'website',
                  'logo'
                )
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control','placeholder':'Company Name'}),
            'address_line_1':forms.TextInput(attrs={'class': 'form-control','placeholder':'Line 1'}),
            'address_line_2':forms.TextInput(attrs={'class': 'form-control','placeholder':'Line 2'}),
            'state':forms.TextInput(attrs={'class': 'form-control','placeholder':'State'}),
            'postal_code':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Postal Code'}),
            'country':forms.TextInput(attrs={'class': 'form-control','placeholder':'Country'}),
            'fax':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Fax'}),
            'website':forms.URLInput(attrs={'class': 'form-control','placeholder':'Website'}),
            'logo':forms.FileInput(attrs={'class': 'form-control','placeholder':'Profile Picture'})
                }
    def clean_name(self):
        name=self.cleaned_data['name']
        if name is None:
            raise forms.ValidationError('Invalid Name',code="name")
        return name
    
class HolidayForm(forms.ModelForm):

    class Meta:

        model = Holiday
        fields = ('company',
                  'date',
                  'name'
        )
        widgets = {
            'company':forms.Select(attrs={'class': 'form-control','placeholder':'Company'}),
            'date':DateInput(attrs={'class': 'form-control','placeholder':'date'}),
            'name':forms.Select(attrs={'class': 'form-control','placeholder':'Holiday'}),
        }
        def clean_name(self):
            print("in clean method")
            name = self.cleaned_data['name']
            if Holiday.objects.filter(name=name).exists():
                print("validation error raised")
                raise forms.ValidationError("This name already exist.")
            return name
class WorkTypeForm(forms.ModelForm):

    class Meta:
        
        model = Work_Type
        fields = ('company',
                  'worktype'
        )
        widgets = {
            'company':forms.Select(attrs={'class': 'form-control','placeholder':'Company'}),
            'worktype':forms.Select(attrs={'class': 'form-control','placeholder':'Work Type'}),
            
                  }
        
class DesignationForm(forms.ModelForm):

    class Meta:
        
        model = Designation
        fields = ('company',
                  'designation',
                  'privilege_leave',
                  'casual_leave'
        )
        widgets = {
            'company':forms.Select(attrs={'class': 'form-control','placeholder':'Company'}),
            'designation':forms.Select(attrs={'class': 'form-control','placeholder':'Designation'}),
            'privilege_leave':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Privilege Leave'}),
            'casual_leave':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Privilege Leave'}),
        }
        
class DepartmentForm(forms.ModelForm):

    class Meta:

        model = Department
        fields = ( 'company',
                   'department'
        )
        widgets = {
            'company':forms.Select(attrs={'class': 'form-control','placeholder':'Company'}),
            'department':forms.Select(attrs={'class': 'form-control','placeholder':'Department'}),
        }
        
class JobTypeForm(forms.ModelForm):
    class Meta:

        model = Job_Type
        fields = ('company',
                  'jobtype'
        )
        widgets = {
            'company':forms.Select(attrs={'class': 'form-control','placeholder':'Company'}),
            'jobtype':forms.Select(attrs={'class': 'form-control','placeholder':'Job Type'}),
        }
