from django.shortcuts import render
from django.views import View
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView,
     RedirectView
)
from django.db.models import Q
from accounts.forms import SignupForm
from django.forms.models import modelformset_factory # model form for querysets
from .forms import *
from accounts.tokens import account_activation_token
from students.forms import *
from accounts.models import *
from .models import *
from indexing_unit.models import *
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
import os
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
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
import io, csv
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.decorators import method_decorator
from indexing_unit.utils import *
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import get_user_model


User = get_user_model()



class StaffRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'Indexing Officer':
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class DashboardView(StaffRequiredMixin, DetailView):
    template_name = "institutions/dashboard1.html"

    def get_object(self):
        user = self.request.user
        obj1 = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
        obj = obj1.first()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        # context['obj'] = obj.first()
        context['object'] = obj
        return context




class InstitutionDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
	template_name = "institutions/institution_details.html"
	success_message = "Institution Profiles was created successfully"

	def get_object(self):
		user = self.request.user
		obj1 = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
		obj = obj1.first()
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		obj = self.get_object()
		context['object'] = obj
		return context


class AdmissionQuotaListView(StaffRequiredMixin, ListView):
	template_name = "institutions/admission_quota_list.html"
	def get_queryset(self):
		request = self.request
		user = request.user
		qs = AdmissionQuota.objects.filter(institution = user.get_indexing_officer_profile.institution)
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs 

class AdmissionQuotaDetailView(StaffRequiredMixin, DetailView):
	# queryset = AdmissionQuota.objects.all()
	template_name = "institutions/admission_quota_details.html"

	def get_object(self):
		user = self.request.user
		obj1 = AdmissionQuota.objects.filter(institution = user.get_indexing_officer_profile.institution)
		obj = obj1.first()
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		obj = self.get_object()
		context['object'] = obj
		return context


# class DashboardView(LoginRequiredMixin, View):
#     template_name = "institutions/dashboard1.html"

#     def get(self, request, *args, **kwarg):
#     	user = self.request.user
#     	try:
#     		obj = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
#     		print ("obj:", obj)
#     		if obj.exists():
#     			return obj
#     	except:
#     		raise Http404
    
#     	return render(request, "institutions/dashboard1.html")

# class StudentProfilesListView(LoginRequiredMixin, ListView):
# 	template_name = "institutions/students_profiles_list.html"

	# def get_queryset(self):
	# 	qs = InstitutionProfile.objects.filter(slug=self.kwargs.get('slug'))
	# 	user = self.request.user
	# 	qs1 = InstitutionProfile.objects.filter(slug=self.kwargs.get('slug'), name = user.get_indexing_officer_profile.first().institution)
	# 	try:
	# 		obj = qs1.first().studentprofile_set.all()
	# 		if obj.exists():
	# 			return obj
	# 	except:
	# 		raise Http404

class StudentProfilesListView(StaffRequiredMixin, ListView):
	template_name = "institutions/students_profiles_list.html"

	def get_queryset(self):
		# qs = InstitutionProfile.objects.filter(slug=self.kwargs.get('slug'))
		user = self.request.user
		
		# print ("qs1:", qs1)
		try:
			qs1 = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
			obj = qs1.first().studentprofile_set.all()
			# print ("obj:", obj)
			if obj.exists():
				return obj
		except:
			raise Http404
		

	def get_context_data(self, **kwargs):
	    context = super(StudentProfilesListView, self).get_context_data(**kwargs)
	    user = self.request.user
	    qs1 = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
	    obj = qs1.first().studentprofile_set.all()
	    context['obj'] = obj
	    return context
		

    
def slug_router(request, slug):
    if InstitutionProfile.objects.filter(slug=slug).exists():
        return StudentProfilesListView.as_view()(request, slug=slug)
    elif InstitutionProfile.objects.filter(slug=slug).exists():
        return DashboardView.as_view()(request, slug=slug)
    else:
        return HttpResponseNotFound('404 Page not found')    

def downloadfile(request):
	 base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	 filename = 'students_list.csv'
	 filepath = base_dir + '/static/csv/' + filename
	 thefile = filepath
	 filename = os.path.basename(thefile) 
	 chunk_size = 8192
	 response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'),chunk_size), content_type=mimetypes.guess_type(thefile)[0])
	 response['Content-Length'] = os.path.getsize(thefile)
	 response['Content-Disposition'] = "Attachment;filename=%s" % filename
	 return response

class CreateAcademicSession(StaffRequiredMixin, CreateView):
    template_name = 'store/create_vendor2.html'
    form_class = AcademicSessionModelForm
    success_message = 'Academic Session created Successfully.'


class InstitutionObjectMixin(object):
    model = InstitutionProfile
    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(self.model, slug=slug)
        return obj 



class StudentProfileCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
	def get(self, request, *args, **kwargs):
		template_name = 'institutions/bulk_create_students.html'
		return render(request, template_name)

	def get_context_data(self, request, *args, **kwarg):
		user = self.request.user
		qs1 = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
		obj = qs1.first().studentprofile_set.all()
		context['object'] = obj
			
	def post(self, request, *args, **kwargs):
		user = self.request.user
		institution = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
		quota = AdmissionQuota.objects.filter(institution = user.get_indexing_officer_profile.institution)
		students_qs = institution.first().studentprofile_set.all()
		admission_quota = quota.first()
		academic_session = admission_quota.academic_session
		students_list = students_qs.filter(academic_session = academic_session)
		paramFile = io.TextIOWrapper(request.FILES['students_list'].file)
		portfolio1 = csv.DictReader(paramFile)
		list_of_dict = list(portfolio1)

		try:
			context = {}
			if User.objects.filter(email =['email']).exists():
				messages.error(request, "f'user `{email}` already exists'")
				print(f'user `{email}` already exists')
				return redirect("institutions:create_student_profile")

			if len(students_list) >= int(admission_quota.admission_quota):
				messages.error(request, "Admission Quota exceeded!")				
				print("Admission Quota exceeded")
				return redirect("institutions:create_student_profile")

			objs = [
	            StudentProfile(
	            	student = User.objects.get_or_create(email=row['email'], last_name=row['last_name'], first_name=row['first_name'], middle_name=row['middle_name'], phone_no=row['phone_no'], matric_no=row['matric_no'], password = make_password('Rebelspy1%'),)[0],  # This is foreignkey value
	            	institution=institution.first(),
	            	academic_session = academic_session,
	            )
	            for row in list_of_dict
	         ]

			for obj in objs:
				obj.slug = create_slug3(instance=obj)		

			nmsg = StudentProfile.objects.bulk_create(objs)
			messages.success(request, "Bulk Create of Students successful!")
			returnmsg = {"status_code": 200}
			user = obj.student
			reset_password(user, request)
			return redirect(institution.first().get_student_profiles_list())			
		except Exception as e:
			print('Error While Importing Data: ', e)
			returnmsg = {"status_code": 500}
		return JsonResponse(returnmsg)
		

class StudentProfileCreateView1(StaffRequiredMixin, SuccessMessageMixin, CreateView):
	# success_message = "Bulk Create of %(student)s Students successful"

	# def get_success_message(self, cleaned_data):
	# 	return self.success_message % dict(
    #         cleaned_data,
    #         student=self.object.student,
    #     )

	def get(self, request, *args, **kwargs):
		template_name = 'institutions/bulk_create_students.html'
		return render(request, template_name)

	def get_context_data(self, request, *args, **kwarg):
		user = self.request.user
		qs1 = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
		obj = qs1.first().studentprofile_set.all()
		context['object'] = obj
		
		
	def post(self, request, *args, **kwargs):
		user = self.request.user
		institution = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
		quota = AdmissionQuota.objects.filter(institution = user.get_indexing_officer_profile.institution)
		students_list = institution.first().studentprofile_set.all()
		admission_quota = quota.first()
		# institution = InstitutionProfile.objects.filter(slug=self.kwargs.get('slug'))
		paramFile = io.TextIOWrapper(request.FILES['students_list'].file)
		portfolio1 = csv.DictReader(paramFile)
		list_of_dict = list(portfolio1)

		try:
			context = {}
			if User.objects.filter(email =['email']).exists():
				messages.error(request, "f'user `{email}` already exists'")
				print(f'user `{email}` already exists')
				return redirect("institutions:create_student_profile")

			if len(students_list) >= int(admission_quota.admission_quota):
				messages.error(request, "Admission Quota exceeded!")				
				print("Admission Quota exceeded")
				return redirect("institutions:create_student_profile")

		# print(list_of_dict)
			objs = [
	            StudentProfile(
	            	student = User.objects.get_or_create(email=row['email'], last_name=row['last_name'], first_name=row['first_name'], middle_name=row['middle_name'], phone_no=row['phone_no'], matric_no=row['matric_no'], password = make_password('Rebelspy1%'),)[0],  # This is foreignkey value
	            	institution=institution.first(),
	            )
	            for row in list_of_dict
	         ]
		# try:
		# 	context = {}
		# 	if User.objects.filter(email =['email']).exists():
		# 		messages.error(request, "f'user `{email}` already exists'")
		# 		print(f'user `{email}` already exists')
		# 		return redirect("institutions:create_student_profile")

		# 	if len(students_list) >= int(admission_quota.admission_quota):
		# 		messages.success(request, "Admission Quota exceeded")
		# 		print("Admission Quota exceeded")
		# 		return redirect("institutions:create_student_profile")

			for obj in objs:
				obj.slug = create_slug3(instance=obj)		
			# user.email_user(subject, message, html_message=message)
			# current_site = get_current_site(request)
			# send_mail(subject, message, from_email, to_email, fail_silently=False)

			nmsg = StudentProfile.objects.bulk_create(objs)
			messages.success(request, "Bulk Create of Students successful!")
			returnmsg = {"status_code": 200}
			user = obj.student
			reset_password(user, request)

			# current_site = get_current_site(request)
			# context['domain'] = current_site.domain 
			# context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
			# context['user'] = user 
			# context['token'] = account_activation_token.make_token(user)
			# context["protocol"] = 'https' if request.is_secure() else 'http'
			# subject = 'Password Change Request'
			# html_template = 'accounts/password_reset_email.html'
			# html_message = render_to_string(html_template, context)
			
			# from_email = settings.DEFAULT_FROM_EMAIL
			# to_email = [obj.student.email]
			# message = EmailMessage(subject, html_message, from_email, to_email)
			# message.content_subtype = 'html'
			# message.send()
			# messages.success(request, ('Please Confirm your email to complete registration.'))
			return redirect(institution.first().get_student_profiles_list())			
		except Exception as e:
			# return render(request, 'institutions/bulk_create_students.html')
			print('Error While Importing Data: ', e)
			returnmsg = {"status_code": 500}
		return JsonResponse(returnmsg)
		


class StudentProfileDetailView1(StaffRequiredMixin, DetailView):
	queryset = StudentProfile.objects.all()
	template_name = "institutions/student_profile_details.html"


class StudentProfileDetailView(StaffRequiredMixin, DetailView):
	template_name = "institutions/student_profile_details.html"

	def get_object(self):
		institutionprofile_slug = self.kwargs.get("islug")
		studentprofile_slug = self.kwargs.get("sslug")
		obj = get_object_or_404(StudentProfile, institution__slug = institutionprofile_slug, slug = studentprofile_slug)
		return obj

class StudentIndexingApplicationsListView(StaffRequiredMixin, ListView):
	template_name = "institutions/student_indexing_applications_list.html"
	def get_queryset(self):
		request = self.request
		user = request.user
		qs = StudentIndexing.objects.filter(institution=user.get_indexing_officer_profile.institution, verification_status=1)
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		# return qs  
		#.filter(title__icontains='vid') 
		return qs.filter #(indexing_status=2) 


class StudentIndexingApplicationDetailView(StaffRequiredMixin, DetailView):
	# queryset = StudentIndexing.objects.all()
	template_name = "institutions/student_indexing_details.html"

	def get_object(self):
		institutionprofile_slug = self.kwargs.get("islug")
		studentindexing_slug = self.kwargs.get("sslug")
		obj = get_object_or_404(StudentIndexing, institution__slug = institutionprofile_slug, slug = studentindexing_slug)
		# send_mail('Subject here', 'Here is the message.', 'institute@rrbn.gov.ng', ['chigozie_okaro@yahoo.com'], fail_silently=False)
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		obj = self.get_object()
		context['payment_object'] = obj.indexingpayment_set.first()
		return context


class StudentIndexingApplicationDetails(StaffRequiredMixin, DetailView):
	# queryset = StudentIndexing.objects.all()
	template_name = "institutions/students_indexing_post_application_details.html"

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



def verify_application(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(StudentIndexing, slug=slug)
     payment_object = object.indexingpayment_set.first()
     object.verification_status = 2
     payment_object.payment_status = 2
     object.save()
     payment_object.save()
     context = {}
     context['object'] = object
     messages.success(request, ('Indexing Application Verified'))
     return HttpResponseRedirect(reverse("institutions:student_indexing_application_details", kwargs={'islug': object.institution.slug,
            'sslug': object.slug,}))

     # url_kwargs={
     #        'islug': self.institution.slug,
     #        'sslug': self.slug,
     #    }
     #    return reverse('indexing_unit:student_indexing_details', kwargs=url_kwargs)

     # return reverse("institutions:student_indexing_application_details", kwargs={'islug': self.institution.slug,
     #        'sslug': self.slug,})
     # return render(request, 'institutions/verification_successful.html',context)


def reject_application(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(StudentIndexing, slug=slug)
     payment_object = object.indexingpayment_set.first()
     object.verification_status = 1
     payment_object.payment_status = 1
     object.save()
     payment_object.save()
     context = {}
     context['object'] = object
     messages.error(request, ('Indexing Application Rejected'))
     return HttpResponseRedirect(reverse("institutions:student_indexing_application_details", kwargs={'islug': object.institution.slug,
            'sslug': object.slug,}))


def verify_payment(request, id):
  if request.method == 'POST':
     object = get_object_or_404(IndexingPayment, pk=id)
     object.payment_status = 2
     object.save()
     context = {}
     context['object'] = object
     messages.success(request, ('Indexing Application Payment Verified'))
     return render(request, 'institutions/submitted_payment_details.html',context)


def reject_payment(request, id):
  if request.method == 'POST':
     object = get_object_or_404(IndexingPayment, pk=id)
     object.payment_status = 1
     object.save()
     context = {}
     context['object'] = object
     # messages.error(request, ('Indexing Application Rejected'))
     return render(request, 'institutions/payment_verification_failed.html',context)


def process(request, id):
  if request.method == 'POST':
  	 StudentIndexing.objects.filter(application_status=2).update(application_status=3)
  	 return render(request, 'institutions/generate_invoice.html')



class IndexingVerificationsListView(StaffRequiredMixin, ListView):
	template_name = "institutions/student_indexing_verifications_list.html"
	def get_queryset(self):
		request = self.request
		user = request.user
		qs = StudentIndexing.objects.filter(institution=user.get_indexing_officer_profile.institution)
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(verification_status=2) 



class IndexingVerificationsDetailView(StaffRequiredMixin, DetailView):
	queryset = StudentIndexing.objects.all()
	template_name = "institutions/student_indexing_verifications_details.html"

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



class GenerateInvoiceView(StaffRequiredMixin, ListView):
    template_name = "institutions/generate_invoice.html"
    def get_queryset(self):
    	request = self.request
    	qs = StudentIndexing.objects.all()
    	query = request.GET.get('q')
    	if query:
    		qs = qs.filter(name__icontains=query)
    	return qs.filter(indexing_status=2) 



class IndexingPaymentCreateView(StaffRequiredMixin, CreateView):
    model = IndexingPayment
    template_name = "institutions/student_indexing_fee_payment.html"
    form_class = IndexingPaymentForm



class IndexingPaymentsListView(StaffRequiredMixin, ListView):
	template_name = "institutions/students_indexing_payments_list.html"
	queryset = IndexingPayment.objects.all()
	# def get_queryset(self):
	# 	request = self.request
	# 	qs = IndexingPayment.objects.all()
	# 	query = request.GET.get('q')
	# 	if query:
	# 		qs = qs.filter(name__icontains=query)
	# 	return qs.filter(indexing_status=3) 

class SubmittedPaymentsListView(StaffRequiredMixin, ListView):
	template_name = "institutions/submitted_payments_list.html"
	# queryset = IndexingPayment.objects.all()

	def get_queryset(self):
		user = self.request.user
		try:
			obj = IndexingPayment.objects.filter(institution = user.get_indexing_officer_profile.institution, payment_status=1)
			print ("obj:", obj)
			if obj.exists():
				return obj
		except:
			raise Http404


class VerifiedPaymentsListView(StaffRequiredMixin, ListView):
	template_name = "institutions/verified_payments_list.html"
	
	# def get_queryset(self):
	# 	user = self.request.user
	# 	try:
	# 		obj = IndexingPayment.objects.filter(institution = user.get_indexing_officer_profile.institution, payment_status=2)
	# 		print ("obj:", obj)
	# 		if obj.exists():
	# 			return obj
	# 	except:
	# 		raise Http404
	def get_queryset(self):
		request = self.request
		user = request.user
		qs = IndexingPayment.objects.filter(institution=user.get_indexing_officer_profile.institution, payment_status=2)
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs


class InstitutionsPaymentsListView(StaffRequiredMixin, ListView):
	template_name = "institutions/institutions_payments_list.html"
	
	def get_queryset(self):
		user = self.request.user
		try:
			obj = InstitutionPayment.objects.filter(institution = user.get_indexing_officer_profile.institution)
			print ("obj:", obj)
			if obj.exists():
				return obj
		except:
			raise Http404



class IndexedStudentsListView(StaffRequiredMixin, ListView):
	template_name = "institutions/indexed_students_list.html"
	def get_queryset(self):
		user = self.request.user
		qs = IssueIndexing.objects.filter(institution = user.get_indexing_officer_profile.institution)
		query = self.request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs 

	def get_context_data(self, **kwargs):
	    context = super(IndexedStudentsListView, self).get_context_data(**kwargs)
	    user = self.request.user
	    institutions = InstitutionProfile.objects.filter(name = user.get_indexing_officer_profile.institution)
	    students = IssueIndexing.objects.filter(institution__in=institutions)
	    context = {
	    'institutions':institutions,
	    'students':students,
	    }
	    print ("context:", context)
	    return context
	    print ("context:", context)





class StudentIndexingPaymentDetailView(StaffRequiredMixin, DetailView):
	queryset = IndexingPayment.objects.all()
	template_name = "institutions/submitted_payment_details.html"


class IndexingPaymentsDetails(StaffRequiredMixin, TemplateView):
    template_name = "institutions/students_indexing_payments_details.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(IndexingPaymentsDetails, self).get_context_data(*args, **kwargs)
        context['object'] = IndexingPayment.objects.all()
        context['obj'] = InstitutionProfile.objects.filter(indexing_status=1)
        return context

class InstitutionPaymentCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = InstitutionPayment
    template_name = "institutions/institutions_indexing_payment.html"
    form_class = InstitutionPaymentModelForm
    success_message = "%(institution)s Institution Indexing Payment Submission Successful"

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            institution=self.object.institution.name,
        )

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(InstitutionPaymentCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        payment = form.save(commit=False)
        user = self.request.user
        institution = InstitutionProfile.objects.get(name=user.get_indexing_officer_profile.institution)
        # form.instance.institution = institution
        payment.institution = institution
        payment.save()
        return super(InstitutionPaymentCreateView, self).form_valid(form)

	    
    # def form_valid(self, form):
    #     user = self.request.user
    #     institution = InstitutionProfile.objects.get(name=user.get_indexing_officer_profile.institution)
    #     form.instance.institution = institution
    #     form.save()
    #     return super(InstitutionPaymentCreateView, self).form_valid(form)    
        


class InstitutionsIndexingPaymentDetailView(StaffRequiredMixin, DetailView):
	queryset = InstitutionPayment.objects.all()
	template_name = "institutions/institutions_payment_details.html"



class StudentIndexingNumberDetailView(StaffRequiredMixin, DetailView):
    queryset = IssueIndexing.objects.all()
    template_name = "institutions/students_indexing_number_details.html"


# class InstitutionPaymentCreateView(LoginRequiredMixin, CreateView):
#     model = InstitutionPayment
#     template_name = "institutions/institutions_payment.html"
#     form = InstitutionPaymentModelForm
#     IndexingPaymentFormset = modelformset_factory(IndexingPayment, form=IndexingPaymentsModelForm)
    

#     def get(self, request, *args, **kwargs):
#     	form = InstitutionPaymentModelForm
#     	IndexingPaymentFormset = modelformset_factory(IndexingPayment, form=IndexingPaymentsModelForm, extra=0,)
#     	form = self.form()
#     	user = self.request.user
#     	qs = IndexingPayment.objects.filter(payment_status=2)
#     	formset = IndexingPaymentFormset(queryset=qs)
    	
#     	return render(request, self.template_name, {'form':form, 'formset':formset})

#     def form_valid(self, form):
#         payment = form.save(commit=False)
#         user = self.request.user
#         student_profile = StudentProfile.objects.get(student = user)
#         institution = InstitutionProfile.objects.get(name = student_profile.institution)
#         # student_indexing = StudentIndexing.objects.get(student_profile = student_profile)
#         payment.institution = institution
#         # payment.student_indexing = student_indexing 
#         # payment.student_profile = student_profile
#         # payment.reg_no = reg_no
#         payment.save()
#         return super(InstitutionPaymentCreateView, self).form_valid(form)



    # user = request.user
    # qs = IndexingPayment.objects.filter(institution = user.get_indexing_officer_profile.institution, payment_status=2)
    # formset = IndexingPaymentFormset(queryset=qs)

    # AppFormSet = formset_factory(EmployeeAppForm)

    # formset = AppFormSet(initial=[
    # {
    #     'id': app.id,
    #     'app': app.name,
    #     'access': Access.objects.filter(employeeapps_app=app, employeeapps_employee=employee).first(),
    #     'status': EmployeeApps.objects.filter(employee=employee, app=app).first().status,
    # } for app in App.objects.all()
	# ])

    # def get(self, request, *args, **kwargs):
    # 	form = self.form_class()
    # 	user = self.request.user
    # 	form.fields["students"].queryset = IndexingPayment.objects.filter(institution = user.get_indexing_officer_profile.institution, payment_status=2)
    # 	return render(request, self.template_name, {'form':form})
    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     user = self.request.user
    #     institution = InstitutionProfile.objects.get(name = user.get_indexing_officer_profile.institution)
    #     instance.institution = institution
    #     return super(InstitutionPaymentCreateView, self).form_valid(form)







