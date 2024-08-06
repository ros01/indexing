from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin
from institutions.models import *

class InstitutionPaymentForm(DynamicFormMixin, forms.Form):


	def academic_session_label(form):
		form['academic_session'].label = "Academic Session"
		return form['academic_session'].label

	academic_session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all(),
        # initial = AcademicSession.objects.first()
    )


	institution = forms.ModelChoiceField(
        queryset=InstitutionProfile.objects.all(),
        # initial = InstitutionProfile.objects.first()
    )

def __init__(self, *args, **kwargs):
       super(InstitutionPaymentForm, self).__init__(*args, **kwargs)
       
       form['id_academic_session'].label = "Select Academic Session"
       form['institution'].label = "Select Institution" 


class InstitutionPaymentForm1(DynamicFormMixin, forms.Form):

	def institution_payment_choices(form):
		academic_session = form['academic_session'].value()
		institution = form['institution'].value()
		return InstitutionPayment.objects.filter(academic_session=academic_session, institution=institution)

	def initial_institution_payment(form):
		academic_session = form['academic_session'].value()
		institution = form['institution'].value()
		return InstitutionPayment.objects.filter(academic_session=academic_session, institution=institution)     


	academic_session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all(),
	 initial = AcademicSession.objects.first()
    )


	institution = forms.ModelChoiceField(
        queryset=InstitutionProfile.objects.all(),
        initial = InstitutionProfile.objects.first()
    )


	institution_payments = DynamicField(
        forms.ModelChoiceField,
        queryset=institution_payment_choices,
        initial=initial_institution_payment
    )



	
	