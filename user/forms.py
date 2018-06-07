from django import forms
from company.models import Designation, Department
from company.models import Job_Type
from .models import Employee,Salary_History
from .models import Designation_History,Department_History
from .models import Job_Type_History
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DateInput(forms.DateInput):
    input_type = 'date'
class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('profile_pic','address','emailid','office_emailid','Dob','gender','contact', 'alter_Contact','joining_date', 'salary')
             
        
        widgets = {
            
            'address':forms.TextInput(attrs={'class': 'form-control','placeholder':'Address'}),
            'Dob':DateInput(attrs={'class': 'form-control','placeholder':'DOB'}),
            'contact':forms.TextInput(attrs={'class': 'form-control','placeholder':'Contact'}),
            'alter_Contact':forms.TextInput(attrs={'class': 'form-control','placeholder':'Alternate Contact'}),
            'emailid':forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email-ID'}),
            'office_emailid':forms.EmailInput(attrs={'class': 'form-control','placeholder':'Office Email-ID'}),
            'gender':forms.Select(attrs={'class': 'form-control','placeholder':'Gender'}),
            'profile_pic':forms.FileInput(attrs={'class': 'form-control','placeholder':'Profile Picture'}),
            'joining_date':DateInput(attrs={'class': 'form-control','placeholder':'Joining Date'}),
            'salary':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Name'})

}


class DesignationForm(forms.ModelForm):
    class Meta:
        
        model = Designation_History
        fields = ('designation',)

        widgets = {
                    'designation':forms.Select(attrs={'class': 'form-control','placeholder':'Designation'})
                  }
                     
    def __init__(self, *args, **kwargs):
        company_id=kwargs.pop('company',False)
        super(DesignationForm, self).__init__(*args, **kwargs)

        if company_id:
            self.fields['designation'] = forms.ModelChoiceField(
            queryset=Designation.objects.filter(company=company_id),
            widget=forms.Select(attrs={'class':'form-control'})
        )
                   
    
class DepartmentForm(forms.ModelForm):
    
    class Meta:
    
        model = Department_History
        fields = ('department',)

        widgets = {
                    'department':forms.Select(attrs={'class': 'form-control','placeholder':'Address'})
                  }
    def __init__(self, *args, **kwargs):
        
        company_id=kwargs.pop('company',False)
        super(DepartmentForm, self).__init__(*args, **kwargs)
    
        if company_id:
            self.fields['department'] = forms.ModelChoiceField(
            queryset=Department.objects.filter(company=company_id),
            widget=forms.Select(attrs={'class':'form-control'})
        )
        


        
class JobTypeForm(forms.ModelForm):

    class Meta:
        model = Job_Type_History
        fields = ('job_type',)

        widgets = {
                    'job_type':forms.Select(attrs={'class': 'form-control'})
                  }

    def __init__(self, *args, **kwargs):
        company_id=kwargs.pop('company',False)
        super(JobTypeForm, self).__init__(*args, **kwargs)

        if company_id:
            self.fields['job_type'] = forms.ModelChoiceField(
            queryset=Job_Type.objects.filter(company=company_id),
            widget=forms.Select(attrs={'class':'form-control'})
        )


        
class SalaryForm(forms.ModelForm):
      class Meta:
        model = Salary_History
        fields = ('basic_percentage','hra_percentage','conveyance_allowance','special_allowance','proffessional_tax','income_tax')

        widgets = {
                    'basic_percentage':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Basic '}),
                    'hra_percentage':forms.NumberInput(attrs={'class': 'form-control','placeholder':'HRA'}),
                    'conveyance_allowance':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Conveyance Allowance'}),
                    'special_allowance':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Special Allowance'}),
                    'proffessional_tax':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Proffessional Tax'}),                              'income_tax':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Income Tax'})
                   }

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2')
        
        widgets = {
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder':'UserName'}),
            'password1':forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}),
            'password2':forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Re-Type Password'})
            }
    
    def __init__(self, *args, **kwargs):
                
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['placeholder']="Password"
        self.fields['password2'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['placeholder']="Confirm Password"
