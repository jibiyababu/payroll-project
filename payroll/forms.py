from django import forms

from .models import Employee

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('name','address','Dob','contact','alter_Contact','emailid','gender')
