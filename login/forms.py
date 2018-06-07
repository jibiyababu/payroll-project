from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserLogin
from user.models import Employee
class LoginForm(forms.ModelForm):
    class Meta:
        
        model = User
        fields = ('username','password')
    
    def clean(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')
        # user = authenticate(username=username, password=password)

        # if user is None:
        #     raise forms.ValidationError('Invalid Credentials')
        # self.cleaned_data['username'] = user
        # self.user_obj=user
        
                    
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2')

        widgets = {
            'username':forms.TextInput(attrs={'class': 'form-control','placeholder':'UserName'}),
            'password1':forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}),
            'password2':forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Re-Type Password'})
            }
       
class DateInput(forms.DateInput):
    input_type = 'date'

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('address','Dob', 'contact', 'alter_Contact', 'emailid', 'gender', 'profile_pic', 'joining_date', 'salary')
        
        widgets = {

            'address':forms.TextInput(attrs={'class': 'form-control','placeholder':'Address'}),
            'Dob':DateInput(attrs={'class': 'form-control','placeholder':'DOB'}),
            'contact':forms.TextInput(attrs={'class': 'form-control','placeholder':'Contact'}),
            'alter_Contact':forms.TextInput(attrs={'class': 'form-control','placeholder':'Alternate Contact'}),
            'emailid':forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email-ID'}),
            'gender':forms.Select(attrs={'class': 'form-control','placeholder':'Gender'}),
            'profile_pic':forms.FileInput(attrs={'class': 'form-control','placeholder':'Profile Picture'}),
            'joining_date':DateInput(attrs={'class': 'form-control','placeholder':'Joining Date'}),
           
            'salary':forms.NumberInput(attrs={'class': 'form-control','placeholder':'Name'})

}
