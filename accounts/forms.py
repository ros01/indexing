from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .choices import * 
from .models import *


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from django.contrib.auth import get_user_model
User = get_user_model()


class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices = ROLE, widget=forms.Select(), required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'phone_no', 'password1', 'password2','role')

    def __init__(self, *args, **kwargs):
       super(SignupForm, self).__init__(*args, **kwargs)
       self.fields['first_name'].label = "First Name"
       self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name"
       self.fields['middle_name'].label = "Middle Name"
       self.fields['last_name'].label = "Last Name"
       self.fields['last_name'].widget.attrs['placeholder'] = "Enter Last Name"
       self.fields['phone_no'].label = "Phone Number"
       self.fields['phone_no'].widget.attrs['placeholder'] = "Enter Phone Number"
       self.fields['email'].label = "Email"
       self.fields['email'].widget.attrs['placeholder'] = "Enter Email"



