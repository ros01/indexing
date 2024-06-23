from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from institutions.choices import * 
from accounts.models import *
from institutions.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin

from django.contrib.auth import get_user_model
User = get_user_model()




class UtmeGradeModelForm1(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
      
    class Meta:
         model = UtmeGrade
         # fields = ('examination_body', 'course_1', 'course_1_grade', 'course_2', 'course_2_grade', 'course_3', 'course_3_grade', 'course_4', 'course_4_grade', 'course_5', 'course_5_grade')
         fields = ('examination_body', 'physics_score', 'chemistry_score', 'biology_score', 'english_score', 'mathematics_score', 'utme_grade_result')     
         widgets = {
         'matric_no': forms.TextInput(attrs={'readonly': True}),
         'examination_body': forms.TextInput(attrs={'readonly': True}),
         # 'student_profile': forms.HiddenInput(),

            }

    def __init__(self, *args, **kwargs):                                  
       super(UtmeGradeModelForm, self).__init__(*args, **kwargs)

       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       # self.fields['student_profile'].label = ""
       self.fields['utme_grade_result'].label = "Upload Result in PDF or Jpeg format"
       self.fields['utme_grade_result'].widget.attrs['placeholder'] = "PDF or Jpeg format"
       # self.fields['matric_no'].label = "Matric Number"
       self.fields['examination_body'].label = "Exam Body"
       self.fields['physics_score'].label = "Physics Score"
       self.fields['chemistry_score'].label = "Chemistry Score"
       self.fields['biology_score'].label = "Biology Score"
       self.fields['english_score'].label = "English Score"
       self.fields['mathematics_score'].label = "Mathematics Score"
       # self.fields['room_design_score'].label = "Room Design"
      
       

    def save(self):

      if not self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class GceAlevelsModelForm1(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
      
    class Meta:
         model = GceAlevels
         # fields = ('examination_body', 'course_1', 'course_1_grade', 'course_2', 'course_2_grade', 'course_3', 'course_3_grade', 'course_4', 'course_4_grade', 'course_5', 'course_5_grade')
         fields = ('examination_body', 'physics_score', 'chemistry_score', 'biology_score', 'gce_alevels_result')
         

         widgets = {
         # 'matric_no': forms.TextInput(attrs={'readonly': True}),
         # 'student_profile': forms.HiddenInput(),

            }

    def __init__(self, *args, **kwargs):                                  
       super(GceAlevelsModelForm, self).__init__(*args, **kwargs)

       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       # self.fields['student_profile'].label = ""
       self.fields['gce_alevels_result'].label = "Upload Result in PDF or Jpeg format"
       self.fields['gce_alevels_result'].widget.attrs['placeholder'] = "PDF or Jpeg format"
       self.fields['examination_body'].label = "Exam Body"
       self.fields['physics_score'].label = "Physics Score"
       self.fields['chemistry_score'].label = "Chemistry Score"
       self.fields['biology_score'].label = "Biology Score"
       # self.fields['matric_no'].label = "Matric Number"
       # self.fields['room_design_score'].widget.attrs['placeholder'] = "(Max Score = 10)"
       

    def save(self):

      if not self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance



class DegreeResultModelForm1(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
      
    class Meta:
         model = DegreeResults
         fields = ('degree_type', 'course', 'course_grade', 'degree_result')
         

         widgets = {
         # 'matric_no': forms.TextInput(attrs={'readonly': True}),
         # 'student_profile': forms.HiddenInput(),

            }

    def __init__(self, *args, **kwargs):                                  
       super(DegreeResultModelForm, self).__init__(*args, **kwargs)

       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       # self.fields['student_profile'].label = ""
       self.fields['degree_result'].label = "Upload Result in PDF or Jpeg format"
       self.fields['degree_result'].widget.attrs['placeholder'] = "PDF or Jpeg format"
       self.fields['degree_type'].label = "Degree Type"
       self.fields['course_grade'].label = "Course Grade"
       self.fields['matric_no'].label = "Matric Number"
       # self.fields['room_design_score'].widget.attrs['placeholder'] = "(Max Score = 10)"
       

    def save(self):

      if not self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance



# class DeGradeModelForm(forms.ModelForm):
      
#     class Meta:
#          model = DeGrade
#          fields = ('student', 'course_1', 'course_1_grade', 'course_2', 'course_2_grade', 'course_3', 'course_3_grade')
         

#          widgets = {
#             # 'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
#             }

#     def __init__(self, *args, **kwargs):
#        super(DeGradeModelFormModelForm, self).__init__(*args, **kwargs)


# class TransferGradeModelForm(forms.ModelForm):
      
#     class Meta:
#          model = TransferGrade
#          fields = ('student', 'course_1', 'course_1_grade', 'course_2', 'course_2_grade', 'course_3', 'course_3_grade')
         

#          widgets = {
#             # 'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
#             }

#     def __init__(self, *args, **kwargs):
#        super(TransferGradeModelForm, self).__init__(*args, **kwargs)



class GceAlevelsModelForm(forms.ModelForm):
      
    class Meta:
         model = GceAlevels
         # fields = ('examination_body', 'course_1', 'course_1_grade', 'course_2', 'course_2_grade', 'course_3', 'course_3_grade', 'course_4', 'course_4_grade', 'course_5', 'course_5_grade')
         fields = ('examination_body', 'physics_score', 'chemistry_score', 'biology_score', 'gce_alevels_result')
         

         widgets = {
         # 'matric_no': forms.TextInput(attrs={'readonly': True}),
         # 'student_profile': forms.HiddenInput(),

            }

    def __init__(self, *args, **kwargs):                                  
       super(GceAlevelsModelForm, self).__init__(*args, **kwargs)

       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       # self.fields['student_profile'].label = ""
       # self.fields['admission_letter'].label = "Upload Admission Letter in PDF or Jpeg format"
       self.fields['gce_alevels_result'].label = "Upload GCE A'Levels Result in PDF or Jpeg format"
       self.fields['gce_alevels_result'].widget.attrs['placeholder'] = "PDF or Jpeg format"
       self.fields['examination_body'].label = "Exam Body"
       self.fields['physics_score'].label = "Physics Score"
       self.fields['chemistry_score'].label = "Chemistry Score"
       self.fields['biology_score'].label = "Biology Score"
       # self.fields['matric_no'].label = "Matric Number"
       # self.fields['room_design_score'].widget.attrs['placeholder'] = "(Max Score = 10)"
       



class DegreeResultModelForm(forms.ModelForm):
      
    class Meta:
         model = DegreeResults
         fields = ('degree_type', 'course', 'institution', 'course_grade', 'degree_result')
         

         widgets = {
         # 'matric_no': forms.TextInput(attrs={'readonly': True}),
         # 'student_profile': forms.HiddenInput(),

            }

    def __init__(self, *args, **kwargs):                                  
       super(DegreeResultModelForm, self).__init__(*args, **kwargs)

       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       # self.fields['student_profile'].label = ""
       # self.fields['admission_letter'].label = "Upload Admission Letter in PDF or Jpeg format"
       self.fields['degree_result'].label = "Upload Degree Result in PDF or Jpeg format"
       self.fields['degree_result'].widget.attrs['placeholder'] = "PDF or Jpeg format"
       self.fields['institution'].label = "Institution of Study"
       self.fields['degree_type'].label = "Degree Type"
       self.fields['course_grade'].label = "Course Grade"
       # self.fields['matric_no'].label = "Matric Number"
       # self.fields['room_design_score'].widget.attrs['placeholder'] = "(Max Score = 10)"
       



class TransferGradeModelForm(forms.ModelForm):
      
    class Meta:
         model = TransferGrade
         fields = ('course', 'institution', 'degree_type', 'year_of_study', 'course_grade', 'academic_transcript')
         

         widgets = {
         # 'matric_no': forms.TextInput(attrs={'readonly': True}),
         # 'student_profile': forms.HiddenInput(),

            }

    def __init__(self, *args, **kwargs):                                  
       super(TransferGradeModelForm, self).__init__(*args, **kwargs)

       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       # self.fields['student_profile'].label = ""
       # self.fields['admission_letter'].label = "Upload Admission Letter in PDF or Jpeg format"
       self.fields['academic_transcript'].label = "Upload Academic Transcript in PDF format"
       self.fields['academic_transcript'].widget.attrs['placeholder'] = "PDF format"
       self.fields['institution'].label = "Institution of Study"
       self.fields['degree_type'].label = "Degree Type"
       self.fields['year_of_study'].label = "Year of Study"
       self.fields['course_grade'].label = "Course Grade"
       # self.fields['matric_no'].label = "Matric Number"
       # self.fields['room_design_score'].widget.attrs['placeholder'] = "(Max Score = 10)"
       




class StudentIndexingModelForm(forms.ModelForm):
      
    class Meta:
         model = StudentIndexing
         fields = ('academic_session', 'admission_type', 'utme_grade')
         

         widgets = {
            # 'contact_address': forms.Textarea(attrs={'rows':2, 'cols':3}),    
            }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StudentIndexingModelForm, self).__init__(*args, **kwargs)
        # self.fields['utme_grade_result'].label = "Upload UTME Result"

    # def clean(self,  **kwargs):
    #     cleaned_data = self.cleaned_data
    #     request = self.request
    #     user = request.user
    #     reg_no = user.reg_no
    #     student_profile = StudentProfile.objects.filter(student=self.user)    
    #     if  StudentIndexing.objects.filter(reg_no=reg_no,        
    #                                student_profile=self.student_profile).exists():
    #         raise ValidationError(
    #               'Solution with this Name already exists for this problem')

    #     # Always return cleaned_data
    #     return cleaned_data



class UtmeGradeModelForm(forms.ModelForm):
    ADMISSION_TYPE = (
    (False, 'No'),
    ('2', 'GCE A Levels'),
    ('3', 'Degree'),
    ('4', 'Transfer'),
    )

    # direct_entry = forms.CheckboxSelectMultiple(choices = ADMISSION_TYPE)

    # [(False, 'No'),(True, 'GCE A Levels'), (True, 'Degree'), (False, 'Transfer')]
    direct_entry = forms.CharField(
        widget=forms.RadioSelect(choices=ADMISSION_TYPE),
        required=False
        )
   
      
    class Meta:
         model = UtmeGrade
         fields = ('examination_body', 'physics_score', 'chemistry_score', 'biology_score', 'english_score', 'mathematics_score', 'utme_grade_result')     
         widgets = {
         # 'matric_no': forms.TextInput(attrs={'readonly': True}),
         # 'examination_body': forms.TextInput(attrs={'readonly': True}),
         # 'student_profile': forms.HiddenInput(),

            }

    def __init__(self, *args, **kwargs):                                  
       super(UtmeGradeModelForm, self).__init__(*args, **kwargs)

       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       # self.fields['student_profile'].label = ""
       # self.fields['admission_letter'].label = "Upload Admission Letter in PDF or Jpeg format"
       self.fields['utme_grade_result'].label = "Upload UTME Result in PDF or Jpeg format"
       self.fields['utme_grade_result'].widget.attrs['placeholder'] = "PDF or Jpeg format"
       # self.fields['matric_no'].label = "Matric Number"
       self.fields['examination_body'].label = "Exam Body"
       self.fields['physics_score'].label = "Physics Score"
       self.fields['chemistry_score'].label = "Chemistry Score"
       self.fields['biology_score'].label = "Biology Score"
       self.fields['english_score'].label = "English Score"
       self.fields['mathematics_score'].label = "Mathematics Score"
       self.fields['direct_entry'].label = "Direct Entry Admission?"
       


class IndexingModelForm(forms.ModelForm):
    # order   = forms.IntegerField(widget=forms.TextInput())
    # admission_type = forms.ChoiceField(choices = ADMISSION_TYPE, widget=forms.Select(), required=True)
    # admission_type = forms.RadioSelect(choices = ADMISSION_TYPE, widget=forms.CheckboxSelectMultiple())
    
   


    class Meta:
        model = StudentIndexing
        fields = [
            # 'institution',
            # 'student_profile',
            # 'utme_grade',
            # 'gce_alevels',
            # 'degree_result',
            # 'academic_session',
            'admission_letter',
            
                ]
        widgets = {
         # 'institution': forms.HiddenInput(),
         # 'student_profile': forms.HiddenInput(),
         # 'academic_session': forms.HiddenInput(),
         # 'admission_type': forms.SelectMultiple(),
         # 'matric_no': forms.TextInput(attrs={'readonly': True}), 
         # 'institution': forms.HiddenInput(),
         # 'student_profile': forms.TextInput(attrs={'readonly': True}),
         # 'utme_grade': forms.HiddenInput(),
         # 'gce_alevels': forms.HiddenInput(),
         # 'degree_result': forms.HiddenInput(),
         
         
         } 


    def __init__(self, *args, **kwargs):
       super(IndexingModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                
            })
       #
       # self.fields['matric_no'].label = "Matric Number"
       self.fields['admission_letter'].label = "Upload Admission Letter in PDF or Jpeg format"
       # self.fields['academic_session'].label = "Academic Session"
      

    def clean_matric_no(self):  
        matric_no = self.cleaned_data.get("matric_no")
        if User.objects.filter(matric_no =['matric_no']).exists():
        # new = User.objects.filter(matric_no = matric_no)  
        # if new.count():  
            raise ValidationError("Student with this Matric Number Already Exist")  
        return matric_no  

    









