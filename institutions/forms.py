from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .choices import * 
from accounts.models import *
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth import get_user_model
User = get_user_model()



# class SignupForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name', 'password1', 'password2')



#     def __init__(self, *args, **kwargs):
#        super(SignupForm, self).__init__(*args, **kwargs)
#        self.fields['first_name'].label = "First Name"
#        self.fields['last_name'].label = "Last Name"
#        self.fields['email'].label = "Email Address"
#        self.fields['email'].widget.attrs['placeholder'] = "enter email that will serve as your username"
#        #self.fields['application_type'].label = "Application Type"
#        #self.fields['application_type'].widget.attrs['placeholder'] = "Select Application Type"


class StudentProfileUpdateModelForm(forms.ModelForm):
      
    class Meta:
         model = StudentProfile
         fields = ('sex', 'dob', 'marital_status', 'nationality', 'state_of_origin', 'lga', 'contact_address')
         

         widgets = {
            'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),
            'dob': DatePickerInput(),
            
         }

    def __init__(self, *args, **kwargs):
       super(StudentProfileUpdateModelForm, self).__init__(*args, **kwargs)
       self.fields['marital_status'].label = "Marital Status"
       self.fields['state_of_origin'].label = "State of Origin"
       self.fields['lga'].label = "Local Government Area"
       self.fields['dob'].label = "Date of Birth"
       self.fields['contact_address'].label = "Contact Address"
       




class StudentProfileModelForm(forms.ModelForm):
      
    class Meta:
         model = StudentProfile
         fields = ('academic_session', 'sex', 'dob', 'marital_status', 'nationality', 'state_of_origin', 'lga', 'contact_address')
         

         widgets = {
            'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),
            'dob': DatePickerInput(),
            
         }

    def __init__(self, *args, **kwargs):
       super(StudentProfileModelForm, self).__init__(*args, **kwargs)
       self.fields['marital_status'].label = "Marital Status"
       self.fields['state_of_origin'].label = "State of Origin"
       self.fields['lga'].label = "Local Government Area"
       self.fields['dob'].label = "Date of Birth"
       self.fields['contact_address'].label = "Contact Address"
       self.fields['academic_session'].label = "Select Academic Session"


class IndexingPaymentModelForm(forms.ModelForm):
      
    class Meta:
         model = IndexingPayment
         fields = ('academic_session', 'rrr_number', 'receipt_number', 'payment_amount', 'payment_method', 'payment_receipt')
         # widgets = {
         #    'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}), 
         #    }
    def __init__(self, *args, **kwargs):
       super(IndexingPaymentModelForm, self).__init__(*args, **kwargs)
       self.fields['academic_session'].label = "Academic Session"
       self.fields['rrr_number'].label = "RRR Number"
       self.fields['rrr_number'].widget.attrs['placeholder'] = "Optional (Enter RRR Number if available)"
       self.fields['receipt_number'].label = "Receipt Number"
       self.fields['receipt_number'].widget.attrs['placeholder'] = "Optional (Enter Receipt Number if available)"
       self.fields['payment_amount'].label = "Payment Amount"
       self.fields['payment_method'].label = "Payment Method"
       self.fields['payment_receipt'].label = "Payment Receipt"
       self.fields['payment_receipt'].widget.attrs['placeholder'] = "PDF or Jpeg format"



class IndexingPaymentsModelForm(forms.ModelForm):
      
    class Meta:
         model = IndexingPayment
         fields = ('student_indexing',)
         # widgets = {
         #    'student_indexing': forms.CheckboxSelectMultiple(),
         #    }


         
    def __init__(self, *args, **kwargs):
       super(IndexingPaymentsModelForm, self).__init__(*args, **kwargs)
       self.fields['student_indexing'].label = "Selected Students for Indexing Payments Submission"
       # self.fields['rrr_number'].label = "RRR Number"
       # self.fields['receipt_number'].label = "Receipt Number"
       # self.fields['payment_amount'].label = "Payment Amount"
       # self.fields['payment_method'].label = "Payment Method"
       # self.fields['payment_receipt'].label = "Payment Receipt"


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, member):
        """ Customises the labels for checkboxes"""
        return "%s" % member.name



class InstitutionPaymentModelForm(forms.ModelForm):
    students_payments = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple())
    
    class Meta:
         model = InstitutionPayment
         fields = ('students_payments', 'academic_session', 'rrr_number', 'payment_amount', 'payment_method', 'payment_receipt')  
    

    def __init__(self, *args, **kwargs):
      
       
       self.request = kwargs.pop('request')
       super(InstitutionPaymentModelForm, self).__init__(*args, **kwargs)
       user = self.request.user
       academic_session = self.request.GET.get('academic_session')
       self.fields['students_payments'].queryset = IndexingPayment.objects.filter(institution = user.get_indexing_officer_profile.institution, student_indexing__verification_status = 2, payment_verification_status=1, academic_session = academic_session)
       # self.fields['students_payments'].queryset = IndexingPayment.objects.filter(institution = user.get_indexing_officer_profile.institution, student_indexing__verification_status = 2, payment_verification_status=1)
       self.fields['academic_session'].label = "Academic Session"
       self.fields['rrr_number'].label = "RRR Number"
       self.fields['payment_amount'].label = "Payment Amount"
       self.fields['payment_method'].label = "Payment Method"
       self.fields['payment_receipt'].label = "Payment Receipt (Jpeg or PDF)"
       self.fields['payment_receipt'].widget.attrs['placeholder'] = "Jpeg or PDF"
       self.fields['students_payments'].label = "Select Students for Institution Indexing Payment"
  
    


      



class IndexingPaymentForm(forms.ModelForm):
      
    class Meta:
         model = IndexingPayment
         fields = ('institution', 'academic_session', 'rrr_number', 'receipt_number', 'payment_amount', 'payment_method', 'payment_receipt')
         

         widgets = {
            # 'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
            }

    def __init__(self, *args, **kwargs):
       super(IndexingPaymentForm, self).__init__(*args, **kwargs)


# class StudentProfileModelForm(forms.ModelForm):
      
#     class Meta:
#          model = StudentProfile
#          fields = ('student', 'sex', 'dob', 'marital_status', 'nationality', 'state_of_origin', 'lga', 'home_address', 'contact_address')
         

#          widgets = {
#             'home_address': forms.Textarea(attrs={'rows':2, 'cols':3}),
#             'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
#             }

#     def __init__(self, *args, **kwargs):
#        super(StudentProfileModelForm, self).__init__(*args, **kwargs)
#        self.fields['student'].label = "Hospital Name"
#        self.fields['student'].widget.attrs['placeholder'] = "enter Hospital Name"
#        self.fields['rc_number'].label = "RC Number"
#        self.fields['rc_number'].widget.attrs['placeholder'] = "leave Blank if unavailable"
#        self.fields['phone_no'].label = "Mobile Telephone Number"
#        self.fields['phone_no'].widget.attrs['placeholder'] = "enter GSM Number"
#        self.fields['state'].label = "State of Location"
#        self.fields['state'].widget.attrs['placeholder'] = "enter State of Location"
#        self.fields['city'].label = "City of Location"
#        self.fields['city'].widget.attrs['placeholder'] = "Enter City of Location"
#        self.fields['contact_address'].label = "Contact Address"
#        self.fields['contact_address'].widget.attrs['placeholder'] = "Enter Contact Address"


