from django import forms
from django.contrib.auth.models import User
from testApp.models import Case
from django.contrib.auth.forms import UserCreationForm
#from phonenumber_field.formfields import PhoneNumberField

class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']
class RegisterNewCaseForm(forms.ModelForm):
    class Meta:
        model=Case
        fields='__all__'
