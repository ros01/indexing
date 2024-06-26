from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import MultipleChoiceField
from django.forms.models import ModelMultipleChoiceField
from django.contrib.admin.widgets import ForeignKeyRawIdWidget 
from accounts.models import *
from .models import *
from institutions.models import *
from dal import autocomplete
from bootstrap_datepicker_plus.widgets import DatePickerInput

class IndexingOfficerProfileForm(forms.ModelForm):
    # order   = forms.IntegerField(widget=forms.TextInput())
    
    
    
    class Meta:
        model = IndexingOfficerProfile
        # fields = "__all__"
        fields = ('indexing_officer', 'institution')
            
            
       
        # widgets = {

        # 'institution': autocomplete.ModelSelect2(url='indexing_unit:institution_autocomplete')
        
        # }


    # def __init__(self, *args, **kwargs):
    #    super(IndexingOfficerProfileForm, self).__init__(*args, **kwargs)
    #    for name in self.fields.keys():
    #         self.fields[name].widget.attrs.update({
                
    #         })
       #
       # self.fields['accreditation_type'].label = "Accreditation Type"

class AcademicSessionModelForm(forms.ModelForm):
      
    class Meta:
         model = AcademicSession
         fields = ('name',)
         
         widgets = {
            # 'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
            }

    def __init__(self, *args, **kwargs):
       super(AcademicSessionModelForm, self).__init__(*args, **kwargs)

# class SelectInstitutionModelForm(forms.ModelForm):
      
#     class Meta:
#          model = InstitutionProfile
#          fields = ('institution_type',)

#          INSTITUTION_TYPE = (
#                 ('University', 'University' ),
#                 ('College of Health', 'College of Health'),
#          )
         
#          widgets = {
#                 'institution_type': forms.Select(choices=INSTITUTION_TYPE,)
#             }

#     def __init__(self,  *args, **kwargs):
#        super(SelectInstitutionModelForm, self).__init__(*args, **kwargs)
#        self.initial['institution_type'] = 'University'
#        self.fields['institution_type'].empty_label = '---Please select your color---'

class SelectInstitutionForm(forms.Form):
    INSTITUTION_TYPE = (
                ('University', 'University' ),
                ('College of Health', 'College of Health'),
         )

    institution_type = forms.ChoiceField(choices=INSTITUTION_TYPE)

class InstitutionProfileForm(forms.ModelForm):
    
    
    class Meta:
        model = InstitutionProfile
        fields = [
            'name',
            'email',
            'phone_no',
            'institution_type',
            'accreditation_score',
            'accreditation_date',
            'accreditation_type',
            'accreditation_due_date',
            'address',
                ]
        widgets = {
        'address': forms.Textarea(attrs={'rows':1, 'cols':12}),
        "accreditation_date": DatePickerInput(),
        "accreditation_due_date": DatePickerInput(),
  
        
        }

       

    def __init__(self, *args, **kwargs):
       super(InstitutionProfileForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                
            })
       #
       self.fields['accreditation_type'].label = "Accreditation Type"
       self.fields['accreditation_score'].label = "Accreditation Score"
       self.fields['accreditation_date'].label = "Accreditation Date"
       self.fields['accreditation_due_date'].label = "Accreditation Due Date"
       self.fields['institution_type'].label = "Institution Type"
       # self.fields['accreditation_date'].widget.attrs['placeholder'] = "Click Calendar button to enter Accreditation Date"
       

 
class AdmissionQuotaForm(forms.ModelForm):
    # order   = forms.IntegerField(widget=forms.TextInput())
    class Meta:
        model = AdmissionQuota
        fields = [
            'institution',
            'academic_session',
            'admission_quota',
            
            
                ]
        widgets = {
        
        }

    def __init__(self, *args, **kwargs):
       super(AdmissionQuotaForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                
            })
       #
       self.fields['academic_session'].label = "Academic Session"



class IssueIndexingForm(forms.ModelForm):
    # order   = forms.IntegerField(widget=forms.TextInput())
    class Meta:
        model = IssueIndexing
        fields = [
            'institution',
            'student_profile',
            'academic_session',
            'student_indexing',
            'index_number',
            'matric_no'
                ]
        widgets = {
         'institution': forms.HiddenInput(),
         'student_profile': forms.HiddenInput(),
         'academic_session': forms.HiddenInput(),
         'student_indexing': forms.HiddenInput(),
         'matric_no': forms.TextInput(attrs={'readonly': True}), 
         # 'student_profile': forms.HiddenInput(),
         # 'student_indexing': forms.HiddenInput(),
         # 'requisition': forms.TextInput(attrs={'readonly': True}), 
         
         } 


    def __init__(self, *args, **kwargs):
       super(IssueIndexingForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                
            })
       #
       self.fields['matric_no'].label = "Matric No"
       self.fields['index_number'].label = "Student Indexing Number"
       

