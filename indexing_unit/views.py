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
from .forms import *
from registration.forms import *
from institutions.models import *
from institutions.models import *
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
from indexing_unit.utils import *



from django.contrib.auth import get_user_model
User = get_user_model()

from dal import autocomplete


class StaffRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'Indexing Unit':
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class InstitutionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return InstitutionProfile.objects.none()

        qs = InstitutionProfile.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class DashboardView(StaffRequiredMixin, ListView):
	#queryset = InstitutionProfile.objects.all()
	template_name = "indexing_unit/dashboard1.html"

	def get_queryset(self):
		request = self.request
		qs = InstitutionProfile.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(DashboardView, self).get_context_data(*args, **kwargs)
	# 	context['random_number'] = random.randint(100, 10000)
	# 	print(context)
	# 	return context


class AcademicSessionCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    template_name = "indexing_unit/create_academic_session.html"
    form_class = AcademicSessionModelForm
    success_message = "%(name)s Academic Session created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class AcademicSessionDetailView(StaffRequiredMixin, DetailView):
	queryset = AcademicSession.objects.all()
	template_name = "indexing_unit/academic_session_details.html"



class AcademicSessionListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/academic_session_list.html"
	def get_queryset(self):
		request = self.request
		qs = AcademicSession.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs 



class InstitutionCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = InstitutionProfile
    template_name = "indexing_unit/register_institution.html"
    form_class = InstitutionProfileForm
    success_message = "%(name)s Institution Profile was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )



# class InstitutionCreateView(CreateView):
# 	user_form = SignupForm
# 	indexing_officer_form = IndexingOfficerProfileForm
# 	institution_form = InstitutionProfileForm
# 	template_name = 'indexing_unit/register_institution.html'
	


class IndexingOfficerCreateView1(CreateView):
    model = IndexingOfficerProfileForm
    template_name = "indexing_unit/create_indexing_officer1.html"
    form_class = IndexingOfficerProfileForm



class IndexingOfficerCreateView2(CreateView):
	model = User
	form_class = SignupForm
	# indexing_officer_form = IndexingOfficerProfileForm
	template_name = 'indexing_unit/create_indexing_officer.html'
	success_url = "/"
	template_name1 = 'indexing_unit/indexing_officer_details.html'



class IndexingOfficerCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
	model = User
	user_form = SignupForm
	form = IndexingOfficerProfileForm
	template_name = 'indexing_unit/create_indexing_officer.html'
	template_name1 = 'indexing_unit/indexing_officer_details.html'

	success_message = "%(last_name)s Indexing Officer Profile was created successfully"

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(
            cleaned_data,
            last_name=self.object.last_name,
        )

	def get(self, request, *args, **kwargs):
		user_form = self.user_form()
		form  = self.form()
		return render(request, self.template_name, {'user_form':user_form, 'form':form})

	def post(self, request, *args, **kwargs):
		user_form = self.user_form(request.POST)
		form  = self.form (request.POST)
		
		if user_form.is_valid() and form.is_valid():
			user = user_form.save(commit=False)
			user.is_active = True
			user.save()
			indexing_officer = form.save(commit=False)
			IndexingOfficerProfile.objects.create(
                indexing_officer = user,
                institution = indexing_officer.institution,
                )
			indexing_officer = IndexingOfficerProfile.objects.filter(indexing_officer=user).first()
			user = user
			reset_password(user, request)
			return redirect(indexing_officer.get_absolute_url())

	   	# 	return redirect('index')  	
	   	
		print(request.POST)
		return render(request, self.template_name, {'user_form':user_form, 'form':form})
    


class IndexingOfficerDetailView(StaffRequiredMixin, DetailView):
	queryset = IndexingOfficerProfile.objects.all()
	template_name = "indexing_unit/indexing_officer_details.html"

	# def get_object(self):
	# 	institutionprofile_slug = self.kwargs.get("islug")
	# 	studentindexing_slug = self.kwargs.get("sslug")
	# 	obj = User.objects.filter(role='Indexing Officer').first()
	# 	return obj

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	obj = self.get_object()
	# 	context['payment_object'] = obj.indexingpayment_set.first()
	# 	return context
# qs = User.objects.filter(role='Indexing Officer')



class IndexingOfficerUpdateView (StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = SignupForm
    template_name = "indexing_unit/update_indexing_officer.html"
    # success_message = "Student Profile Update Successful"

    success_message = "%(indexing_officer)s  Update Successful"
    def get_object(self, queryset=None):
    	pk = self.kwargs.get("pk")
    	user = User.objects.get(id=pk)
    	return user

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            indexing_officer=self.object.get_full_name,
        )

    # def get(self, request, id = None, *args, **kwargs):
    # 	context = {}
    # 	pk = self.kwargs.get("pk")
    # 	obj = User.objects.get(id = pk)
    # 	if obj is not None:
    #     	# user_form = self.user_form(instance=obj)
    #     	form  = self.form(instance=obj)
    # 	return render(request, self.template_name, {'form':form})

 
    def get_success_url(self):
        # obj = self.get_object()
        # return reverse("indexing_unit:indexing_officer_detail" object.pk)
        return reverse("indexing_unit:indexing_officers_list") 

       


def activate_user(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(IndexingOfficerProfile, slug=slug)
     indexing_object = object.indexing_officer
     indexing_object.is_active = True
     indexing_object.save()
     context = {}
     context['object'] = object
     messages.success(request, ('Indexing Officer is now Active'))
     return HttpResponseRedirect(reverse("indexing_unit:indexing_officer_detail", kwargs={'slug': object.slug,}))


def deactivate_user(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(IndexingOfficerProfile, slug=slug)
     indexing_object = object.indexing_officer
     indexing_object.is_active = False
     indexing_object.save()
     context = {}
     context['object'] = object
     messages.success(request, ('Indexing Officer has now been deactivated'))
     return HttpResponseRedirect(reverse("indexing_unit:indexing_officer_detail", kwargs={'slug': object.slug,}))







class UniversitiesListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/institutions_list1.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionProfile.objects.filter(institution_type='University')
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs  #.filter(title__icontains='vid')

class CollegesListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/institutions_list1.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionProfile.objects.filter(institution_type='College of Health')
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs  #.filter(title__icontains='vid')



# class InstitutionList1View(StaffRequiredMixin, ListView):
# 	template_name = "indexing_unit/institutions_list1.html"
# 	def get_queryset(self):
# 		request = self.request
# 		qs = InstitutionProfile.objects.filter(institution_type='University')
# 		query = request.GET.get('q')
# 		if query:
# 			qs = qs.filter(name__icontains=query)
# 		return qs  #.filter(title__icontains='vid') 

 
class IndexingOfficerListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/indexing_officers_list.html"
	def get_queryset(self):
		request = self.request
		# qs = User.objects.filter(role='Indexing Officer')
		qs = IndexingOfficerProfile.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs  #.filter(title__icontains='vid')

class AdmissionQuotaListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/admission_quota_list.html"
	def get_queryset(self):
		request = self.request
		qs = AdmissionQuota.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs 


class InstitutionCreateView1(CreateView):
	user_form = SignupForm
	indexing_officer_form = IndexingOfficerProfileForm
	institution_form = InstitutionProfileForm
	template_name = 'indexing_unit/create_institution_profile.html'
	
	
	
	def get(self, request, *args, **kwargs):
		user_form = self.user_form()
		indexing_officer_form  = self.indexing_officer_form()
		institution_form  = self.institution_form()
		return render(request, self.template_name, {'user_form':user_form, 'institution_form':institution_form, 'indexing_officer_form':indexing_officer_form})

	def post(self, request, *args, **kwargs):
		user_form = self.user_form(request.POST)
		indexing_officer_form  = self.indexing_officer_form (request.POST)
		institution_form  = self.institution_form (request.POST)


		if user_form.is_valid() and institution_form.is_valid() and indexing_officer_form.is_valid():
	   		user = user_form.save(commit=False)
	   		user.is_active = True
	   		user.save()
	   		institution = institution_form.save()
	   		indexing_officer = indexing_officer_form.save(commit=False)
	   		IndexingOfficerProfile.objects.create(
                indexing_officer = user,
                institution = institution,
                )
	   		return redirect('index')
	   	
	   	
		print(request.POST)
		return render(request, self.template_name, {'user_form':user_form, 'institution_form':institution_form, 'indexing_officer_form':indexing_officer_form})




class InstitutionDetailView(StaffRequiredMixin, SuccessMessageMixin, DetailView):
	queryset = InstitutionProfile.objects.all()
	template_name = "indexing_unit/institution_details.html"
	success_message = "Institution Profiles was created successfully"
	# def get_success_message(self, cleaned_data):
	# 	return self.success_message % dict(
    #         cleaned_data,
    #         name=self.object.name,
    #     )

 
class AdmissionQuotaCreateView(StaffRequiredMixin, CreateView):
    model = AdmissionQuota
    template_name = "indexing_unit/assign_admission_quota.html"
    form_class = AdmissionQuotaForm


    # def form_invalid(self, form):
    # 	print(form.errors)
    # 	return self.render_to_response(self.get_context_data(form=form))



class AdmissionQuotaDetailView(StaffRequiredMixin, DetailView):
	queryset = AdmissionQuota.objects.all()
	template_name = "indexing_unit/admission_quota_details.html"



class AdmissionQuotaUpdateView (StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AdmissionQuota
    form_class = AdmissionQuotaForm
    template_name = "indexing_unit/assign_admission_quota.html"
    # success_message = "Student Profile Update Successful"

    success_message = "%(institution)s Admision Quota Update Successful"

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            institution=self.object.institution.name,
        )

 
    def get_success_url(self):
        obj = self.get_object()
        return reverse("indexing_unit:admission_quota_list")

class IndexingApplicationsListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/students_indexing_applications_list.html"
	def get_queryset(self):
		request = self.request
		qs = StudentIndexing.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(indexing_status=2) 


class IndexingVerificationsDetailView(StaffRequiredMixin, DetailView):
	queryset = StudentIndexing.objects.all()
	template_name = "indexing_unit/student_indexing_verification_details.html"





class IndexNumberIssuanceList(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/index_number_issuance_list.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionPayment.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(payment_status=2) 

@login_required
def institutions_list(request):
	form = SelectInstitutionModelForm()
	context = {'form': form}
	return render(request, 'indexing_unit/select_institution.html', context)

@login_required
def universities_list(request):
	
	context = {
	    'universities_list':universities_list,
	    }
	return render(request, 'partials/universities_list.html', context)


class InstitutionListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/select_institution.html"
	def get_queryset(self):
		institutions = InstitutionProfile.objects.all() 
		return institutions

	def get_context_data(self, **kwargs):
		context = super(InstitutionListView, self).get_context_data(**kwargs)
		filter_set = self.get_queryset()
		form = SelectInstitutionForm()
		institution_type = form['institution_type'].value()
		if self.request.GET.get('institution_type'):
			institution_type = self.request.GET.get('institution_type')
			if institution_type == "University":
				filter_set = filter_set.filter(institution_type=institution_type)
			elif institution_type == "College of Health":
				filter_set = filter_set.filter(institution_type=institution_type)
		context['form'] = SelectInstitutionForm()	
		context['institution'] = filter_set
		return context


class InstitutionSearchView(ListView):
	template_name = "indexing_unit/institutions_list1.html"
	def get_queryset(self):
		institutions = InstitutionProfile.objects.all() 
		return institutions

	def get_context_data(self, **kwargs):
		context = super(InstitutionSearchView, self).get_context_data(**kwargs)
		filter_set = self.get_queryset()
		form = SelectInstitutionForm()
		institution_type = form['institution_type'].value()
		if self.request.GET.get('institution_type'):
			institution_type = self.request.GET.get('institution_type')
			if institution_type == "University":
				filter_set = filter_set.filter(institution_type=institution_type)
			elif institution_type == "College of Health":
				filter_set = filter_set.filter(institution_type=institution_type)
		context['form'] = SelectInstitutionForm()	
		context['institution'] = filter_set
		return context


class InstitutionsIndexedStudentsList(ListView):
	template_name = "indexing_unit/indexed_students_list.html"
	def get_queryset(self):
		institutions = InstitutionProfile.objects.all()
		qs = IssueIndexing.objects.filter(institution__in=institutions)
		return qs	
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


class InstitutionsIndexedStudentsListView(ListView):
	template_name = "indexing_unit/institutions_indexed_students_list.html"
	def get_queryset(self):
		institutions = InstitutionProfile.objects.all()
		qs = IssueIndexing.objects.filter(institution__in=institutions)
		return qs
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



class InstitutionsIndexingStudentsListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/institutions_indexing_students_list.html"
	def get_queryset(self):
		request = self.request
		qs = IssueIndexing.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs 

	def get_context_data(self, **kwargs):
	    context = super(InstitutionsIndexingStudentsListView, self).get_context_data(**kwargs)
	    institutions = InstitutionProfile.objects.all()
	    students = IssueIndexing.objects.filter(institution__in=institutions)
	    context = {
	    'institutions':institutions,
	    'students':students,
	    }
	    print ("context:", context)
	    return context
	    print ("context:", context)

    	 	

class IssueIndexNumberDetails(StaffRequiredMixin, DetailView):
	queryset = StudentIndexing.objects.all()
	template_name = "indexing_unit/assign_index_number_detail.html"

class IndexObjectMixin(object):
    model = StudentIndexing
    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(self.model, slug=slug)
        return obj 


class IssueIndexNumber1(CreateView):
    model = IssueIndexing
    template_name = "indexing_unit/issue_indexing_number.html"
    form_class = IssueIndexingForm

    def form_valid(self, form):
        payment = form.save(commit=False)
        user = self.request.user
        institution = InstitutionProfile.objects.get(name=user.get_indexing_officer_profile.institution)
        payment.institution = institution
        payment.save()
        return super(InstitutionPaymentCreateView, self).form_valid(form)



class IssueIndexingNumber(StaffRequiredMixin, CreateView, IndexObjectMixin):
    model = IssueIndexing
    template_name = "indexing_unit/issue_index_number.html"
    form_class = IssueIndexingForm

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
        kwargs['initial']['reg_no'] = self.student_indexing.student_profile.student.reg_no
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




class IssuedIndexingApplications(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/issued_indexing_applications_list.html"
	def get_queryset(self):
		request = self.request
		qs = IssueIndexing.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs

class InstitutionsPaymentsListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/institutions_payments_list.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionPayment.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(payment_status=1)


class InstitutionsVerifiedPaymentsList(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/institutions_verified_payments_list.html"
	def get_queryset(self):
		request = self.request
		qs = InstitutionPayment.objects.all()
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(payment_status=2)


class InstitutionsIndexingPaymentDetailView(StaffRequiredMixin, DetailView):
	queryset = InstitutionPayment.objects.all()
	template_name = "indexing_unit/institutions_payment_details.html"

	# def get_queryset(self):
	# 	request = self.request
	# 	# qs = InstitutionPayment.objects.prefetch_related(Prefetch('students_payments', queryset=IndexingPayment.objects.filter(payment_status = 2))).filter(payment_status=2)
	# 	qs_object = InstitutionPayment.objects.filter(students_payments__payment_status= 3)
	# 	qs = IndexingPayment.objects.filter(institutionpayment__in=qs_object)
	# 	# print('Hello', qs)
	# 	query = request.GET.get('q')
	# 	if query:
	# 		qs = qs.filter(name__icontains=query)
	# 	return qs


	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	object_list = self.get_queryset()
	# 	context['object_list'] = object_list
	# 	return context

class InstitutionsIndexingPreIssueDetailView(StaffRequiredMixin, DetailView):
	queryset = InstitutionPayment.objects.prefetch_related(Prefetch('students_payments', queryset=IndexingPayment.objects.filter(payment_status = 2)))
	template_name = "indexing_unit/institutions_indexing_pre_issue_details.html"


class VerifiedPaymentsListView(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/verified_payments_list.html"
	
	def get_queryset(self):
		user = self.request.user
		try:
			obj = InstitutionPayment.objects.filter(payment_status=2)
			print ("obj:", obj)
			if obj.exists():
				return obj
		except:
			raise Http404

class InstitutionsPaymentsListView1(StaffRequiredMixin, ListView):
	template_name = "indexing_unit/institutions_payments_list.html"
	
	def get_queryset(self):
		user = self.request.user
		try:
			obj = InstitutionPayment.objects.filter(institution = user.get_indexing_officer_profile.institution, payment_status=1)
			print ("obj:", obj)
			if obj.exists():
				return obj
		except:
			raise Http404

class IssuedIndexingApplicationsDetails(StaffRequiredMixin, DetailView):
	queryset = IssueIndexing.objects.all()
	template_name = "indexing_unit/issued_indexing_applications_details.html"



class StudentIndexingApplicationDetailView(StaffRequiredMixin, DetailView):
    # queryset = StudentIndexing.objects.all()
    template_name = "indexing_unit/student_indexing_application_details.html"

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

  
class StudentsIndexingApplicationDetails(StaffRequiredMixin, DetailView):
    # queryset = StudentIndexing.objects.all()
    template_name = "indexing_unit/students_indexing_application_details.html"

    def get_object(self):
    	institutionprofile_slug = self.kwargs.get("islug")
    	studentindexing_slug = self.kwargs.get("sslug")
    	obj = get_object_or_404(StudentIndexing, institution__slug = institutionprofile_slug, slug = studentindexing_slug)
    	return obj



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
     messages.success(request, ('Indexing Application and Payment Verified'))
     return HttpResponseRedirect(reverse("indexing_unit:student_indexing_details", kwargs={'islug': object.institution.slug,
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
     return HttpResponseRedirect(reverse("indexing_unit:student_indexing_details", kwargs={'islug': object.institution.slug,
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
     return HttpResponseRedirect(reverse("indexing_unit:institutions_indexing_payment_details", kwargs={'slug': object.slug}))
     # return render(request, 'indexing_unit/payment_verification_successful.html',context)


def reject_payment(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(InstitutionPayment, slug=slug)
     object.payment_status = 1
     object.save()
     context = {}
     context['object'] = object
     messages.error(request, ('Institution Payment Rejected'))
     return HttpResponseRedirect(reverse("indexing_unit:institutions_indexing_payment_details", kwargs={'slug': object.slug}))
     # return render(request, 'indexing_unit/payment_verification_failed.html',context)


# def verify(request, id):
#   if request.method == 'POST':
#      object = get_object_or_404(StudentIndexing, pk=id)
#      object.indexing_status = 3
#      object.save()
#      context = {}
#      context['object'] = object
#      # messages.success(request, ('Indexing Application Verified'))
#      return render(request, 'indexing_unit/verifications_successful.html',context)


# def reject(request, id):
#   if request.method == 'POST':
#      object = get_object_or_404(StudentIndexing, pk=id)
#      object.indexing_status = 4
#      object.save()
#      context = {}
#      context['object'] = object
#      # messages.error(request, ('Indexing Application Rejected'))
#      return render(request, 'indexing_unit/verification_failed.html',context)



class StudentIndexingNumberDetailView(StaffRequiredMixin, DetailView):
    queryset = IssueIndexing.objects.all()
    template_name = "indexing_unit/students_indexing_number_details.html"

