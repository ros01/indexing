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
from .forms import *
from indexing_unit.models import *
from django.db import transaction
from django.db.models import F, Q
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



@login_required
def institutions_payments_list(request):
	academic_sessions = AcademicSession.objects.all()
	context = {'academic_sessions': academic_sessions}
	return render(request, 'registration/academic_session_payments.html', context)

@login_required
def payments_list(request):
	academic_session = request.GET.get('academic_session')
	user = request.user
	payments = InstitutionIndexing.objects.filter(academic_session=academic_session, payment_status=1)
	context = {'payments': payments}
	return render(request, 'partials/registration_payments.html', context)


@login_required
def institutions_verified_payments_list(request):
	academic_sessions = AcademicSession.objects.all()
	context = {'academic_sessions': academic_sessions}
	return render(request, 'registration/academic_session_verified_payments.html', context)

@login_required
def verified_payments_list(request):
	academic_session = request.GET.get('academic_session')
	user = request.user
	payments = InstitutionIndexing.objects.filter(academic_session=academic_session, payment_status=2)
	context = {'payments': payments}
	return render(request, 'partials/registration_verified_payments.html', context)


class InstitutionsPaymentsListView(StaffRequiredMixin, ListView):
	template_name = "registration/institutions_payments_list.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionIndexing.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(payment_status=1)


class InstitutionsVerifiedPaymentsList(StaffRequiredMixin, ListView):
	template_name = "registration/institutions_verified_payments_list.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionIndexing.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(payment_status=2)


class InstitutionsIndexingPaymentDetailView(StaffRequiredMixin, DetailView):
	queryset = InstitutionIndexing.objects.all()
	template_name = "registration/institutions_indexing_submission.html"


	# def get_queryset(self):
	# 	# students_payments = IndexingPayment.objects.filter(payment_status= 2)
	# 	qs = InstitutionPayment.objects.all()
	# 	qs1 = qs.filter(students_payments__payment_status = 2)
	# 	print("qs1:", qs1)
	# 	return qs1

class InstitutionsIndexingPaymentVerifiedDetailView(StaffRequiredMixin, DetailView):
	queryset = InstitutionIndexing.objects.all()
	template_name = "registration/institutions_payment_verified_details.html"



@login_required
def students_index_number_list(request):
	form = InstitutionIndexingForm()
	context = {'form': form}
	return render(request, 'registration/academic_session_indexing_list.html', context)
	# academic_sessions = AcademicSession.objects.all()
	# institutions = InstitutionProfile.objects.all()
	# context = {'academic_sessions': academic_sessions, 'institutions': institutions}
	# return render(request, 'registration/academic_session_indexing_list.html', context)

@login_required
def select_institution(request):
	# academic_session = request.GET.get('academic_session')
	institutions = InstitutionProfile.objects.all()
	# user = request.user
	# students_payments = IndexingPayment.objects.filter(payment_status= 3)
	# qs = InstitutionPayment.objects.filter(academic_session=academic_session, students_payments__in=students_payments, payment_status = 2)
	context = {'institutions':institutions, 'is_htmx': True}
	return render(request, 'partials/indexing_numbers_pre_list.html', context)

@login_required
def indexing_numbers_list(request):
	form = InstitutionIndexingForm(request.GET)
	# return HttpResponse(form['institution_payments'])
	
	academic_session = form['institution_payments'].value()
	institution = form['institution_payments'].value()
	print ("Academic Session is:", form['academic_session'].value())
	print ("Institution is:", form['institution'].value())

	academic_session = request.GET.get('academic_session')
	institution = request.GET.get('institution')
	user = request.user
	student_indexing = StudentIndexing.objects.filter(verification_status= 3)
	qs = InstitutionIndexing.objects.filter(student_indexing__in=student_indexing, verification_status = 2)
	print ("Institution Payment Aca:", qs)
	query = qs.filter(Q(academic_session = request.GET.get('academic_session')) & Q(institution = request.GET.get('institution')))
	print ("Institution Payment:", query)
	context = {'query': query}

	# if request.htmx:
		# return render(request, 'partials/indexing_numbers_pre_issue_list.html', context)
	return render(request, 'partials/indexing_numbers_pre_issue_list.html', context)

class IndexNumberIssuanceListView(StaffRequiredMixin, ListView):
	template_name = "registration/institutions_indexing_list.html"
	
	def get_queryset(self):
		student_indexing = StudentIndexing.objects.filter(verification_status= 3)
		qs = InstitutionIndexing.objects.filter(student_indexing__in=student_indexing, payment_status = 2)
		return qs.distinct()


	def get_context_data(self, **kwargs):
		context = super(IndexNumberIssuanceListView, self).get_context_data(**kwargs)
		filter_set = self.get_queryset()
		form = InstitutionPaymentForm()
		academic_session = form['academic_session'].value()
		# print("Academic Session:", academic_session)
		institution = form['institution'].value()
		if self.request.GET.get('academic_session'):
			academic_session = self.request.GET.get('academic_session')
			filter_set = filter_set.filter(academic_session=academic_session)


		if self.request.GET.get('institution'):
			institution = self.request.GET.get('institution')
			filter_set = filter_set.filter(institution=institution)



		context['form'] = InstitutionPaymentForm()	
		context['indexing'] = filter_set
		return context


class IndexNumberIssuanceList(StaffRequiredMixin, ListView):
	template_name = "registration/index_number_issuance_list.html"
	

	# def get(self, request, *args, **kwargs):
	# 	form = InstitutionPaymentForm(self.request.GET)
	# 	academic_session_id = form['institution_payments'].value()
	# 	institution_id = form['institution_payments'].value()
	# def get_queryset(self):
	# 	institutionpayments = InstitutionPayment.objects.filter(payment_status= 2)
	# 	qs = IndexingPayment.objects.filter(institutionpayment__in=institutionpayments, payment_status = 3)
	# 	return qs.distinct()

	def get_queryset(self):
		student_indexing = StudentIndexing.objects.filter(indexing_status= "verified")
		qs = InstitutionIndexing.objects.filter(student_indexing__in=student_indexing, payment_status = 2)
		return qs.distinct()


	def get_context_data(self, **kwargs):
		context = super(IndexNumberIssuanceList, self).get_context_data(**kwargs)
		filter_set = self.get_queryset()
		form = InstitutionPaymentForm()
		academic_session = form['academic_session'].value()
		# print("Academic Session:", academic_session)
		institution = form['institution'].value()
		if self.request.GET.get('academic_session'):
			academic_session = self.request.GET.get('academic_session')
			filter_set = filter_set.filter(academic_session=academic_session)


		if self.request.GET.get('institution'):
			institution = self.request.GET.get('institution')
			filter_set = filter_set.filter(institution=institution)



		context['form'] = InstitutionPaymentForm()	
		context['indexing'] = filter_set
		return context



    # if self.request.GET.get('location'):
    #     location = self.request.GET.get('location')
    #     filter_set = filter_set.filter(location=location)

    # if self.request.GET.get('calibrator'):
    #     calibrator = self.request.GET.get('calibrator')
    #     filter_set = filter_set.filter(calibrator=calibrator)

    # if self.request.GET.get('next_cal_date'):
    #     next_cal_date = self.request.GET.get('next_cal_date')
    #     filter_set = filter_set.filter(next_cal_date__lte=next_cal_date)

    
    # context['title'] = "Gauges "
    # context['types'] = Gauge_Types.objects.all()
    # context['locations'] = Locations.objects.all()
    # context['calibrators'] = Calibrator.objects.all()
    # And so on for more models
    

	


class InstitutionsIndexingPreIssueDetailView(StaffRequiredMixin, DetailView):
	# queryset = InstitutionPayment.objects.prefetch_related(Prefetch('students_payments', queryset=IndexingPayment.objects.filter(payment_status = 3)))
	queryset = InstitutionIndexing.objects.all()
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



class StudentIndexingVerifiedDetails(StaffRequiredMixin, DetailView):
    # queryset = StudentIndexing.objects.all()
    template_name = "registration/student_indexing_verified_details.html"

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


class StudentsPostIndexingDetails(StaffRequiredMixin, DetailView):
    # queryset = StudentIndexing.objects.all()
    template_name = "registration/student_post_indexing_details.html"

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

@login_required
def approve_application(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(StudentIndexing, slug=slug)
     # payment_object = object.indexingpayment_set.first()
     # object.verification_status = 3
     object.indexing_status = "verified"
     # payment_object.payment_status = 3
     object.save()
     # payment_object.save()
     context = {}
     context['object'] = object
     messages.success(request, ('Indexing Application Verified'))
     return HttpResponseRedirect(reverse("registration:student_indexing_details", kwargs={'islug': object.institution.slug,
            'sslug': object.slug,}))
     # return render(request, 'indexing_unit/verification_successful.html',context)

@login_required
def reject_application(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(StudentIndexing,slug=slug)
     # payment_object = object.indexingpayment_set.first()
     object.indexing_status = "board_rejection"
     # payment_object.payment_status = 2
     object.save()
     # payment_object.save()
     context = {}
     context['object'] = object
     messages.error(request, ('Indexing Application Rejected'))
     return HttpResponseRedirect(reverse("registration:student_indexing_details", kwargs={'islug': object.institution.slug,
            'sslug': object.slug,}))
     # return render(request, 'indexing_unit/verification_failed.html',context)

@login_required
def verify_payment(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(InstitutionIndexing, slug=slug)
     object.payment_status = 2
     object.save()
     context = {}
     context['object'] = object
     messages.success(request, ('Institution Payment Verified'))
     return HttpResponseRedirect(reverse("registration:institutions_indexing_payment_verified_details", kwargs={'slug': object.slug}))
     # return render(request, 'indexing_unit/payment_verification_successful.html',context)

@login_required
def reject_payment(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(InstitutionIndexing, slug=slug)
     object.payment_status = 1
     object.save()
     context = {}
     context['object'] = object
     messages.error(request, ('Institution Payment Not Verified'))
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

    # def form_valid(self, form):
    #     indexing = form.save(commit=False)
    #     student_indexing = StudentIndexing.objects.get(student_profile=self.student_profile)
    #     indexing.student_indexing = student_indexing
    #     indexing.save()
    #     return super(IssueIndexingNumber, self).form_valid(form)


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
	    return context
	    

class InstitutionsIndexedStudentsList(StaffRequiredMixin, ListView):
	template_name = "registration/indexed_students_list.html"
	def get_queryset(self):
		institutions = InstitutionProfile.objects.all()
		qs = IssueIndexing.objects.filter(institution__in=institutions)
		return qs
		# students_payments = IndexingPayment.objects.filter(payment_status= 3)
		# qs = InstitutionPayment.objects.filter(students_payments__in=students_payments, payment_status = 2)
		# return qs.distinct()
	def get_context_data(self, **kwargs):
		context = super(InstitutionsIndexedStudentsList, self).get_context_data(**kwargs)
		filter_set = self.get_queryset()
		form = InstitutionPaymentForm()
		academic_session = form['academic_session'].value()
		institution = form['institution'].value()
		if self.request.GET.get('academic_session'):
			academic_session = self.request.GET.get('academic_session')
			filter_set = filter_set.filter(academic_session=academic_session)
		if self.request.GET.get('institution'):
			institution = self.request.GET.get('institution')
			filter_set = filter_set.filter(institution=institution)
		context['form'] = InstitutionPaymentForm()	
		context['indexing'] = filter_set
		return context


class InstitutionsIndexedStudentsListView(StaffRequiredMixin, ListView):
	template_name = "registration/institutions_indexed_students_list.html"
	def get_queryset(self):
		institutions = InstitutionProfile.objects.all()
		qs = IssueIndexing.objects.filter(institution__in=institutions)
		return qs
		# students_payments = IndexingPayment.objects.filter(payment_status= 3)
		# qs = InstitutionPayment.objects.filter(students_payments__in=students_payments, payment_status = 2)
		# return qs.distinct()
	def get_context_data(self, **kwargs):
		context = super(InstitutionsIndexedStudentsListView, self).get_context_data(**kwargs)
		filter_set = self.get_queryset()
		form = InstitutionPaymentForm()
		academic_session = form['academic_session'].value()
		institution = form['institution'].value()
		if self.request.GET.get('academic_session'):
			academic_session = self.request.GET.get('academic_session')
			filter_set = filter_set.filter(academic_session=academic_session)
		if self.request.GET.get('institution'):
			institution = self.request.GET.get('institution')
			filter_set = filter_set.filter(institution=institution)
		context['form'] = InstitutionPaymentForm()	
		context['indexing'] = filter_set
		return context


class StudentIndexingNumberDetailView(StaffRequiredMixin, DetailView):
    queryset = IssueIndexing.objects.all()
    template_name = "registration/students_indexing_number_details.html"








