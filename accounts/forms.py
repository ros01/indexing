from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .choices import * 
from .models import *

from .tokens import account_activation_token
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from django.contrib.auth import get_user_model
User = get_user_model()


class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices = ROLE, widget=forms.Select(), required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'middle_name', 'phone_no', 'password1', 'password2', 'role']


    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string(
            'users/activate_account.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )

        user.email_user(subject, message, html_message=message)

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


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("Passwords doesn't match."),
        'password_length': ("Your password must be 8 caracters minimum."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    confirmation = forms.CharField(label=("Confirm new password"),
                                    widget=forms.PasswordInput)
    def clean_confirmation(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('confirmation')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
            if len(password1)<8:
                raise forms.ValidationError(
                    self.error_messages['password_length'],
                    code='password_length',
                )
        return password2








