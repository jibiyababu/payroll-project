from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User



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
        
                    
            
class DateInput(forms.DateInput):
    input_type = 'date'

