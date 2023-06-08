from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from institutions.choices import * 
from accounts.models import *
from institutions.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from django.contrib.auth import get_user_model
User = get_user_model()




class UtmeGradeModelForm(forms.ModelForm):
      
    class Meta:
         model = UtmeGrade
         fields = ('examination_body', 'course_1', 'course_1_grade', 'course_2', 'course_2_grade', 'course_3', 'course_3_grade', 'course_4', 'course_4_grade', 'course_5', 'course_5_grade')
         

         widgets = {
            # 'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
            }

    def __init__(self, *args, **kwargs):
       super(UtmeGradeModelForm, self).__init__(*args, **kwargs)

class DeGradeModelForm(forms.ModelForm):
      
    class Meta:
         model = DeGrade
         fields = ('student', 'course_1', 'course_1_grade', 'course_2', 'course_2_grade', 'course_3', 'course_3_grade')
         

         widgets = {
            # 'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
            }

    def __init__(self, *args, **kwargs):
       super(DeGradeModelFormModelForm, self).__init__(*args, **kwargs)


class TransferGradeModelForm(forms.ModelForm):
      
    class Meta:
         model = TransferGrade
         fields = ('student', 'course_1', 'course_1_grade', 'course_2', 'course_2_grade', 'course_3', 'course_3_grade')
         

         widgets = {
            # 'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
            }

    def __init__(self, *args, **kwargs):
       super(TransferGradeModelForm, self).__init__(*args, **kwargs)


class StudentIndexingModelForm(forms.ModelForm):
      
    class Meta:
         model = StudentIndexing
         fields = ('academic_session', 'admission_type', 'utme_grade', 'de_grade', 'transfer_grade')
         

         widgets = {
            # 'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
            }

    def __init__(self, *args, **kwargs):
       super(StudentIndexingModelForm, self).__init__(*args, **kwargs)