from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import MultipleChoiceField
from django.forms.models import ModelMultipleChoiceField
from django.contrib.admin.widgets import ForeignKeyRawIdWidget 
from accounts.models import *

from .models import *
from institutions.models import *
from dal import autocomplete


class IndexingOfficerProfileForm(forms.ModelForm):
    # order   = forms.IntegerField(widget=forms.TextInput())
    
    
    
    class Meta:
        model = IndexingOfficerProfile
        fields = ('__all__')
        # fields = [
        #     'indexing_officer',
        #     'institution',
        #         ]
       
        widgets = {

        'institution': autocomplete.ModelSelect2(url='indexing_unit:institution_autocomplete')
        
        }


    # def __init__(self, *args, **kwargs):
    #    super(IndexingOfficerProfileForm, self).__init__(*args, **kwargs)
    #    for name in self.fields.keys():
    #         self.fields[name].widget.attrs.update({
                
    #         })
       #
       # self.fields['accreditation_type'].label = "Accreditation Type"


class InstitutionProfileForm(forms.ModelForm):
    # order   = forms.IntegerField(widget=forms.TextInput())
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
            'address',
                ]
        widgets = {
        'address': forms.Textarea(attrs={'rows':1, 'cols':12}),
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
       self.fields['institution_type'].label = "Institution Type"
       

 
class AdmissionQuotaForm(forms.ModelForm):
    # order   = forms.IntegerField(widget=forms.TextInput())
    class Meta:
        model = AdmissionQuota
        fields = [
            'institution',
            'academic_session',
            'course_1',
            'admission_quota_1',
            'course_2',
            'admission_quota_2',
            
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
            'reg_no'
                ]
        widgets = {
         'institution': forms.HiddenInput(),
         'student_profile': forms.HiddenInput(),
         'academic_session': forms.HiddenInput(),
         'student_indexing': forms.HiddenInput(),
         'reg_no': forms.TextInput(attrs={'readonly': True}), 
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
       self.fields['index_number'].label = "Student Indexing Number"
       

