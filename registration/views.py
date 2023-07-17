from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView
)

import random
from accounts.forms import SignupForm
from indexing_unit.forms import *
from .models import *
from institutions.models import *
from indexing_unit.models import *
from django.db import transaction
from django.db.models import F
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views import static
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from django.views.generic.detail import (
    SingleObjectMixin,
    SingleObjectTemplateResponseMixin,
)
from django.views.generic.edit import FormMixin, ProcessFormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib import messages 
from django.contrib.messages.views import SuccessMessageMixin



from django.contrib.auth import get_user_model
User = get_user_model()

from dal import autocomplete


class StaffRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'Registration':
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class DashboardView(StaffRequiredMixin, ListView):
	#queryset = InstitutionProfile.objects.all()
	template_name = "registration/dashboard.html"

	def get_queryset(self):
		request = self.request
		qs = InstitutionProfile.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs


class InstitutionListView(StaffRequiredMixin, ListView):
	template_name = "registration/institutions_list.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionProfile.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs  #.filter(title__icontains='vid')


class InstitutionDetailView(StaffRequiredMixin, SuccessMessageMixin, DetailView):
	queryset = InstitutionProfile.objects.all()
	template_name = "registration/institution_details.html"
	success_message = "Institution Profiles was created successfully"




class IndexingOfficerListView(StaffRequiredMixin, ListView):
	template_name = "registration/indexing_officers_list.html"
	def get_queryset(self):
		request = self.request
		qs = User.objects.filter(role='Indexing Officer')
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs  #.filter(title__icontains='vid')


class IndexingOfficerDetailView(StaffRequiredMixin, DetailView):
	queryset = IndexingOfficerProfile.objects.all()
	template_name = "registration/indexing_officer_details.html"


class AdmissionQuotaListView(StaffRequiredMixin, ListView):
	template_name = "registration/admission_quota_list.html"
	def get_queryset(self):
		request = self.request
		qs = AdmissionQuota.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs 

class AdmissionQuotaDetailView(StaffRequiredMixin, DetailView):
	queryset = AdmissionQuota.objects.all()
	template_name = "registration/admission_quota_details.html"



class InstitutionsPaymentsListView(StaffRequiredMixin, ListView):
	template_name = "registration/institutions_payments_list.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionPayment.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(payment_status=1)


class InstitutionsVerifiedPaymentsList(StaffRequiredMixin, ListView):
	template_name = "registration/institutions_verified_payments_list.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionPayment.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(payment_status=2)


class InstitutionsIndexingPaymentDetailView(StaffRequiredMixin, DetailView):
	queryset = InstitutionPayment.objects.all()
	template_name = "registration/institutions_payment_details.html"


class IndexNumberIssuanceList(StaffRequiredMixin, ListView):
	template_name = "registration/index_number_issuance_list.html"
	# def get_queryset(self):
	# 	institutionpayments = InstitutionPayment.objects.filter(payment_status= 2)
	# 	qs = IndexingPayment.objects.filter(institutionpayment__in=institutionpayments, payment_status = 3)
	# 	return qs.distinct()

	def get_queryset(self):
		students_payments = IndexingPayment.objects.filter(payment_status= 3)
		qs = InstitutionPayment.objects.filter(students_payments__in=students_payments, payment_status = 2)
		return qs.distinct()

	


class InstitutionsIndexingPreIssueDetailView(StaffRequiredMixin, DetailView):
	# queryset = InstitutionPayment.objects.prefetch_related(Prefetch('students_payments', queryset=IndexingPayment.objects.filter(payment_status = 3)))
	queryset = InstitutionPayment.objects.all()
	template_name = "registration/institutions_indexing_pre_issue_details.html"

	



class StudentsIndexingApplicationDetails(StaffRequiredMixin, DetailView):
    # queryset = StudentIndexing.objects.all()
    template_name = "registration/students_indexing_application_details.html"

    def get_object(self):
    	institutionprofile_slug = self.kwargs.get("islug")
    	studentindexing_slug = self.kwargs.get("sslug")
    	obj = get_object_or_404(StudentIndexing, institution__slug = institutionprofile_slug, slug = studentindexing_slug)
    	return obj

    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	obj = self.get_object()
    	context['payment_object'] = obj.indexingpayment_set.first()
    	return context


class StudentIndexingApplicationDetailView(StaffRequiredMixin, DetailView):
    # queryset = StudentIndexing.objects.all()
    template_name = "registration/student_indexing_application_details.html"

    def get_object(self):
    	institutionprofile_slug = self.kwargs.get("islug")
    	studentindexing_slug = self.kwargs.get("sslug")
    	obj = get_object_or_404(StudentIndexing, institution__slug = institutionprofile_slug, slug = studentindexing_slug)
    	return obj


    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	obj = self.get_object()
    	context['payment_object'] = obj.indexingpayment_set.first()
    	return context


def approve_application(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(StudentIndexing, slug=slug)
     payment_object = object.indexingpayment_set.first()
     object.verification_status = 3
     payment_object.payment_status = 3
     object.save()
     payment_object.save()
     context = {}
     context['object'] = object
     messages.success(request, ('Indexing Application Verified'))
     return HttpResponseRedirect(reverse("registration:student_indexing_details", kwargs={'islug': object.institution.slug,
            'sslug': object.slug,}))
     # return render(request, 'indexing_unit/verification_successful.html',context)


def reject_application(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(StudentIndexing,slug=slug)
     payment_object = object.indexingpayment_set.first()
     object.verification_status = 2
     payment_object.payment_status = 2
     object.save()
     payment_object.save()
     context = {}
     context['object'] = object
     messages.error(request, ('Indexing Application Rejected'))
     return HttpResponseRedirect(reverse("registration:student_indexing_details", kwargs={'islug': object.institution.slug,
            'sslug': object.slug,}))
     # return render(request, 'indexing_unit/verification_failed.html',context)

def verify_payment(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(InstitutionPayment, slug=slug)
     object.payment_status = 2
     object.save()
     context = {}
     context['object'] = object
     messages.success(request, ('Institution Payment Verified'))
     return HttpResponseRedirect(reverse("registration:institutions_indexing_payment_details", kwargs={'slug': object.slug}))
     # return render(request, 'indexing_unit/payment_verification_successful.html',context)


def reject_payment(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(InstitutionPayment, slug=slug)
     object.payment_status = 1
     object.save()
     context = {}
     context['object'] = object
     messages.error(request, ('Institution Payment Rejected'))
     return HttpResponseRedirect(reverse("registration:institutions_indexing_payment_details", kwargs={'slug': object.slug}))



class IndexObjectMixin(object):
    model = StudentIndexing
    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(self.model, slug=slug)
        return obj 



class IssueIndexingNumber(StaffRequiredMixin, SuccessMessageMixin, CreateView, IndexObjectMixin):
    model = IssueIndexing
    template_name = "registration/issue_indexing_number.html"
    form_class = IssueIndexingForm
    success_message = "Student Indexing Number issued successfully for %(name)s"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.student_profile.student.get_full_name,
        )

    def get_initial(self):
        # You could even get the Book model using Book.objects.get here!
        return {
            'student_indexing': self.kwargs["slug"],
            #'license_type': self.kwargs["pk"]
        }

    def get_form_kwargs(self):
        self.student_indexing = StudentIndexing.objects.get(slug=self.kwargs['slug'])
        kwargs = super().get_form_kwargs()
        kwargs['initial']['student_profile'] = self.student_indexing.student_profile
        kwargs['initial']['student_indexing'] = self.student_indexing
        kwargs['initial']['matric_no'] = self.student_indexing.student_profile.student.matric_no
        kwargs['initial']['institution'] = self.student_indexing.institution
        kwargs['initial']['academic_session'] = self.student_indexing.academic_session
        #kwargs['initial']['hospital'] = self.payment.hospital
        
        return kwargs

    def form_valid(self, form):
        indexing = form.save(commit=False)
        indexing_payment = IndexingPayment.objects.get(student_indexing=self.student_indexing)
        indexing.indexing_payment = indexing_payment
        indexing.save()
        return super(IssueIndexingNumber, self).form_valid(form)


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())



class InstitutionsIndexedStudentsListView(StaffRequiredMixin, ListView):
	template_name = "registration/institutions_indexed_students_list.html"
	def get_queryset(self):
		request = self.request
		qs = IssueIndexing.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs 

	def get_context_data(self, **kwargs):
	    context = super(InstitutionsIndexedStudentsListView, self).get_context_data(**kwargs)
	    institutions = InstitutionProfile.objects.all()
	    students = IssueIndexing.objects.filter(institution__in=institutions)
	    context = {
	    'institutions':institutions,
	    'students':students,
	    }
	    print ("context:", context)
	    return context
	    print ("context:", context)


class StudentIndexingNumberDetailView(StaffRequiredMixin, DetailView):
    queryset = IssueIndexing.objects.all()
    template_name = "registration/students_indexing_number_details.html"








