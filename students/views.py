from django.shortcuts import render
from django.views import View
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView
)
import os
from formtools.wizard.views import SessionWizardView
from formtools.preview import FormPreview
from django.core.files.storage import FileSystemStorage
from .forms import *
from institutions.forms import *
from accounts.forms import SignupForm
from accounts.models import *
from indexing_unit.models import *
from .models import *
from django.forms.models import model_to_dict
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views import static
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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
from institutions.models import *
from django.contrib.auth import get_user_model
User = get_user_model()





class StaffRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'Student':
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request,
            *args, **kwargs)

class DashboardView(StaffRequiredMixin, DetailView):

    template_name = "students/dashboard1.html"

    def get_object(self):
        user = self.request.user
        obj = StudentProfile.objects.filter(student=user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['obj'] = obj.first()
        return context

@login_required
def status(request):
    user = request.user
    if StudentProfile.objects.filter(student = user, indexing_status=1):
        return MyStudentProfileListView.as_view()(request)
    elif StudentProfile.objects.filter(student = user, indexing_status=2):
        return ApplicationList.as_view()(request)
    elif StudentIndexing.objects.filter(student_profile__student = user, verification_status='pending'):
        return MyIndexingApplicationListView.as_view()(request)
    elif StudentIndexing.objects.filter(student_profile__student = user, verification_status='approved'):
        return MyIndexingApplicationListView.as_view()(request)
    # elif IndexingPayment.objects.filter(student_profile__student = user, payment_verification_status=1):
    #     return MyIndexingPaymentListView.as_view()(request)
    elif StudentIndexing.objects.filter(student_profile__student = user, verification_status='approved', indexing_status='indexed'):
        return MyIndexingCompleteListView.as_view()(request)
    else:
         return MyIndexingCompleteListView.as_view()(request)


class MyIndexingApplicationListView(StaffRequiredMixin, ListView):
    template_name = "students/my_indexing_application_list.html"
    def get_queryset(self):
        request = self.request
        qs = StudentIndexing.objects.filter(student_profile__student=request.user)
        query = request.GET.get('q')
        if query:
            qs = qs.filter(student_profile__student__icontains=query)
        return qs 

# class MyIndexingApplicationListView(LoginRequiredMixin, ListView):
#     template_name = "students/my_indexing_application_list.html"
#     def get_queryset(self):
#         request = self.request
#         qs = StudentProfile.objects.all()
#         query = request.GET.get('q')
#         user = self.request.user
#         if query:
#             qs = qs.filter(student__icontains=query)
#         return qs
        # if user.is_authenticated():
        #     qs = qs.owned(user)


class MyStudentProfileListView(StaffRequiredMixin, ListView):
    template_name = "students/my_student_profile_list.html"
    def get_queryset(self):
        request = self.request
        qs = StudentProfile.objects.filter(student=request.user)
        query = request.GET.get('q')
        user = self.request.user
        if query:
            qs = qs.filter(student__icontains=query)
        return qs


class ApplicationList(StaffRequiredMixin, ListView):
    template_name = "students/my_application_list.html"
    def get_queryset(self):
        request = self.request
        qs = StudentProfile.objects.filter(student=request.user)
        query = request.GET.get('q')
        user = self.request.user
        if query:
            qs = qs.filter(student__icontains=query)
        return qs

class IndexingPaymentCreateListView(StaffRequiredMixin, ListView):
    template_name = "students/my_indexing_payment_create_list.html"
    def get_queryset(self):
        request = self.request
        qs = StudentIndexing.objects.filter(student_profile__student=request.user)
        query = request.GET.get('q')
        if query:
            qs = qs.filter(student_profile__student__icontains=query)
        return qs 


class MyStudentProfileDetailView(StaffRequiredMixin, DetailView):
    # queryset = StudentProfile.objects.all()
    template_name = "students/my_student_profile_details.html"


    def get_object(self):
        institutionprofile_slug = self.kwargs.get("islug")
        studentprofile_slug = self.kwargs.get("sslug")
        obj = get_object_or_404(StudentProfile, institution__slug = institutionprofile_slug, slug = studentprofile_slug)
        return obj

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     obj = self.get_object()
    #     context['payment_object'] = obj.indexingpayment_set.first()
    #     return context



class UpdateProfile(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileUpdateModelForm
    template_name = "students/update_profile.html"
    # success_message = "Student Profile Update Successful"

    success_message = "%(student)s Student Profile Update Successful"

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            student=self.object.student.get_full_name,
        )

    def get_object(self):
        institutionprofile_slug = self.kwargs.get("islug")
        studentprofile_slug = self.kwargs.get("sslug")
        obj = get_object_or_404(StudentProfile, institution__slug = institutionprofile_slug, slug = studentprofile_slug)
        return obj

    
    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.indexing_status >2:
            pass
        else:
            instance.indexing_status = 2
        
        return super(UpdateProfile, self).form_valid(form)

    def get_success_url(self):
        obj = self.get_object()
        return reverse("students:my_student_profile_details", kwargs={'islug': obj.institution.slug,
            'sslug': obj.slug,})

class StudentObjectMixin(object):
    model = StudentProfile
    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(self.model, slug=slug)
        return obj 



class WaecResult(StaffRequiredMixin, StudentObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'students/utme_result.html'
    form_class = UtmeGradeModelForm
    success_message = 'UTME Result Entered Successfully'
     
    def get_success_url(self):
        return reverse("students:start_indexing_application", kwargs={"slug": self.object.student_profile.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['student_profile'] = StudentProfile.objects.select_related("student").filter(student = user, indexing_status=2) 
        # context['schedule_qs'] = Schedule.objects.select_related("hospital_name").filter(application_status=4, hospital_name=self.schedule.hospital_name, hospital__license_type = 'Radiography Practice Permit')     
        return context

    def get_initial(self):
        return {
            'student_profile': self.kwargs["slug"],
        }
    
    def get_form_kwargs(self):
        self.student_profile = StudentProfile.objects.get(slug=self.kwargs['slug'])
        kwargs = super().get_form_kwargs()
        kwargs['initial']['student_profile'] = self.student_profile
        kwargs['initial']['matric_no'] = self.student_profile.student.matric_no
        kwargs['initial']['examination_body'] = "WAEC"
        return kwargs
      
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())


class NecoResult(StaffRequiredMixin, StudentObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'students/utme_result.html'
    form_class = UtmeGradeModelForm
    success_message = 'UTME Result Entered Successfully'
     
    def get_success_url(self):
        return reverse("students:start_indexing_application", kwargs={"slug": self.object.student_profile.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['student_profile'] = StudentProfile.objects.select_related("student").filter(student = user, indexing_status=2) 
        # context['schedule_qs'] = Schedule.objects.select_related("hospital_name").filter(application_status=4, hospital_name=self.schedule.hospital_name, hospital__license_type = 'Radiography Practice Permit')     
        return context

    def get_initial(self):
        return {
            'student_profile': self.kwargs["slug"],
        }
    
    def get_form_kwargs(self):
        self.student_profile = StudentProfile.objects.get(slug=self.kwargs['slug'])
        kwargs = super().get_form_kwargs()
        kwargs['initial']['student_profile'] = self.student_profile
        kwargs['initial']['matric_no'] = self.student_profile.student.matric_no
        kwargs['initial']['examination_body'] = "NECO"
        return kwargs
      
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())


class NabtebResult(StaffRequiredMixin, StudentObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'students/utme_result.html'
    form_class = UtmeGradeModelForm
    success_message = 'UTME Result Entered Successfully'
     
    def get_success_url(self):
        return reverse("students:start_indexing_application", kwargs={"slug": self.object.student_profile.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['student_profile'] = StudentProfile.objects.select_related("student").filter(student = user, indexing_status=2) 
        # context['schedule_qs'] = Schedule.objects.select_related("hospital_name").filter(application_status=4, hospital_name=self.schedule.hospital_name, hospital__license_type = 'Radiography Practice Permit')     
        return context

    def get_initial(self):
        return {
            'student_profile': self.kwargs["slug"],
        }
    
    def get_form_kwargs(self):
        self.student_profile = StudentProfile.objects.get(slug=self.kwargs['slug'])
        kwargs = super().get_form_kwargs()
        kwargs['initial']['student_profile'] = self.student_profile
        kwargs['initial']['matric_no'] = self.student_profile.student.matric_no
        kwargs['initial']['examination_body'] = "NABTEB"
        return kwargs
      
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())



class AlevelsResult(StaffRequiredMixin, StudentObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'students/gce_alevels_result.html'
    form_class = GceAlevelsModelForm
    success_message = 'GCE A Levels Results Entered Successfully'
     
    def get_success_url(self):
        return reverse("students:start_indexing_application", kwargs={"slug": self.object.student_profile.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['student_profile'] = StudentProfile.objects.select_related("student").filter(student = user, indexing_status=2) 
        # context['schedule_qs'] = Schedule.objects.select_related("hospital_name").filter(application_status=4, hospital_name=self.schedule.hospital_name, hospital__license_type = 'Radiography Practice Permit')     
        return context

    def get_initial(self):
        return {
            'student_profile': self.kwargs["slug"],
        }
    
    def get_form_kwargs(self):
        self.student_profile = StudentProfile.objects.get(slug=self.kwargs['slug'])
        kwargs = super().get_form_kwargs()
        kwargs['initial']['student_profile'] = self.student_profile
        kwargs['initial']['matric_no'] = self.student_profile.student.matric_no
        # kwargs['initial']['examination_body'] = "NABTEB"
        return kwargs
      
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())


class DegreeResult(StaffRequiredMixin, StudentObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'students/degree_result.html'
    form_class = DegreeResultModelForm
    success_message = 'Degree Results Entered Successfully'
     
    def get_success_url(self):
        return reverse("students:start_indexing_application", kwargs={"slug": self.object.student_profile.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['student_profile'] = StudentProfile.objects.select_related("student").filter(student = user, indexing_status=2) 
        # context['schedule_qs'] = Schedule.objects.select_related("hospital_name").filter(application_status=4, hospital_name=self.schedule.hospital_name, hospital__license_type = 'Radiography Practice Permit')     
        return context

    def get_initial(self):
        return {
            'student_profile': self.kwargs["slug"],
        }
    
    def get_form_kwargs(self):
        self.student_profile = StudentProfile.objects.get(slug=self.kwargs['slug'])
        kwargs = super().get_form_kwargs()
        kwargs['initial']['student_profile'] = self.student_profile
        kwargs['initial']['matric_no'] = self.student_profile.student.matric_no
        # kwargs['initial']['examination_body'] = "NABTEB"
        return kwargs
      
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())


class IndexingApplicationCreateView(StaffRequiredMixin, StudentObjectMixin, CreateView):
    model = StudentIndexing
    template_name = "students/start_indexing_application1.html"
    form_class = IndexingModelForm
    success_message = "%(student_profile)s Indexing Application Submission Successful"

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            student_profile=self.object.student_profile.student.get_full_name,
        )

    def get_initial(self):
        # You could even get the Book model using Book.objects.get here!
        return {
            'student_profile': self.kwargs["slug"],
            #'license_type': self.kwargs["pk"]
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['student_profile'] = StudentProfile.objects.select_related("student").filter(student = user, indexing_status=2) 
        # context['schedule_qs'] = Schedule.objects.select_related("hospital_name").filter(application_status=4, hospital_name=self.schedule.hospital_name, hospital__license_type = 'Radiography Practice Permit')     
        return context

    def get_form_kwargs(self):
        self.student_profile = StudentProfile.objects.get(slug=self.kwargs['slug'])
        kwargs = super().get_form_kwargs()
        kwargs['initial']['student_profile'] = self.student_profile
        kwargs['initial']['matric_no'] = self.student_profile.student.matric_no
        kwargs['initial']['institution'] = self.student_profile.institution
        kwargs['initial']['utme_grade'] = self.student_profile.utmegrade_set.first()
        kwargs['initial']['gce_alevels'] = self.student_profile.gcealevels_set.first()
        kwargs['initial']['degree_result'] = self.student_profile.degreeresults_set.first()
        #kwargs['initial']['hospital'] = self.payment.hospital
        print (kwargs)
        return kwargs

    def clean_matric_no(self):     
        if matric_no.exist:
           raise ValidationError("Matric Number already exists")


    def form_invalid(self, form):
        messages.error(request, 'Form already submitted')
        return self.render_to_response(self.get_context_data())




class IndexingApplicationCreateView0(StaffRequiredMixin, StudentObjectMixin, CreateView):
    model = StudentIndexing
    template_name = "students/start_indexing_application1.html"
    form_class = IndexingModelForm
    success_message = "%(student_profile)s Indexing Application Submission Successful"

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            student_profile=self.object.student_profile.student.get_full_name,
        )

    def get_initial(self):
        # You could even get the Book model using Book.objects.get here!
        return {
            'student_profile': self.kwargs["slug"],
            #'license_type': self.kwargs["pk"]
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['student_profile'] = StudentProfile.objects.select_related("student").filter(student = user, indexing_status=2) 
        # context['schedule_qs'] = Schedule.objects.select_related("hospital_name").filter(application_status=4, hospital_name=self.schedule.hospital_name, hospital__license_type = 'Radiography Practice Permit')     
        return context

    def get_form_kwargs(self):
        self.student_profile = StudentProfile.objects.get(slug=self.kwargs['slug'])
        kwargs = super().get_form_kwargs()
        kwargs['initial']['student_profile'] = self.student_profile
        kwargs['initial']['matric_no'] = self.student_profile.student.matric_no
        kwargs['initial']['institution'] = self.student_profile.institution
        kwargs['initial']['utme_grade'] = self.student_profile.utmegrade_set.first()
        kwargs['initial']['gce_alevels'] = self.student_profile.gcealevels_set.first()
        kwargs['initial']['degree_result'] = self.student_profile.degreeresults_set.first()
        #kwargs['initial']['hospital'] = self.payment.hospital
        print (kwargs)
        return kwargs

    def clean_matric_no(self):     
        if matric_no.exist:
           raise ValidationError("Matric Number already exists")


    def form_invalid(self, form):
        messages.error(request, 'Form already submitted')
        return self.render_to_response(self.get_context_data())



FORMS = [("start_application", IndexingModelForm),
         ("utme_admission", UtmeGradeModelForm),
         ("gce_alevels", GceAlevelsModelForm),
         ("degree_result", DegreeResultModelForm),
         ("transfer_admission", TransferGradeModelForm)]


# def show_business_form(wizard):
#     cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
#     return cleaned_data.get('is_business_guest')




def submit_indexing_application(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('utme_admission') or {'direct_entry': 'none'}
    cleaned_data['direct_entry'] == False


def show_gce_alevels_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('utme_admission') or {'direct_entry': 'none'}
    return cleaned_data['direct_entry'] == '2'


def show_degree_result_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('utme_admission') or {'direct_entry': 'none'}
    return cleaned_data['direct_entry'] == '3'

def show_transfer_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('utme_admission') or {'direct_entry': 'none'}
    return cleaned_data['direct_entry'] == '4'

class StudentIndexingWizardView(SessionWizardView):
    # form_list = [IndexingModelForm, UtmeGradeModelForm, GceAlevelsModelForm, DegreeResultModelForm, TransferGradeModelForm] 
    form_list = [("start_application", IndexingModelForm),
         ("utme_admission", UtmeGradeModelForm),
         ("gce_alevels", GceAlevelsModelForm),
         ("degree_result", DegreeResultModelForm),
         ("transfer_admission", TransferGradeModelForm)]
    template_name = "students/student_indexing.html"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    condition_dict = {'gce_alevels': show_gce_alevels_form,
                      'degree_result': show_degree_result_form,
                      'transfer_admission': show_transfer_form}

    def done(self, form_list, **kwargs):
        self.student_profile = StudentProfile.objects.get(slug=self.kwargs['slug'])
        indexing_form = form_list[0]
        indexing = indexing_form.save(commit=False)
        utme = form_list[1]
        utme_grade = utme.save()
        # gce_alevels = form_list[2]
        # degree_result = form_list[-2]
        # transfer_admission = form_list[-1]


        if utme.cleaned_data['direct_entry'] == '2':
            gce_alevels = form_list[2].save()
            indexing.gce_alevels = gce_alevels
        elif utme.cleaned_data['direct_entry'] == '3':
            degree_result = form_list[2].save()
            indexing.degree_result = degree_result
        elif utme.cleaned_data['direct_entry'] == '4':
            transfer_admission = form_list[2].save()
            indexing.transfer_grade = transfer_admission
        else:
            utme_grade = utme.save()
        
        indexing.utme_grade = utme_grade
        indexing.student_profile = self.student_profile
        indexing.institution = self.student_profile.institution
        indexing.matric_no = self.student_profile.student.matric_no
        indexing.academic_session = self.student_profile.academic_session
        indexing.save()
        url_kwargs={
            'islug': indexing.institution.slug,
            'sslug': indexing.slug,
        }

        return HttpResponseRedirect(reverse('students:my_indexing_application_details', kwargs=url_kwargs)) 


        # if utme.cleaned_data['direct_entry'] == '2':
        #     gce_alevels = form_list[2].save()
        #     indexing.gce_alevels = gce_alevels
        # if utme.cleaned_data['direct_entry'] == '3':
        #     degree_result = form_list[-2].save()
        #     indexing.degree_result = degree_result
        # if utme.cleaned_data['direct_entry'] == '4':
        #     transfer_admission = form_list[4].save()
        #     indexing.transfer_grade = transfer_admission
       
        # utme = form_list[1].save()
        # indexing.utme_grade = utme
        # indexing.student_profile = self.student_profile
        # indexing.institution = self.student_profile.institution
        # indexing.matric_no = self.student_profile.student.matric_no
        # indexing.save()

            
        # student_profile.save()
        # utme = form_list[-1].save(commit=False)
        # utme.student_profile = utme
        # guest_form = form_list[0]
        # if guest_form.cleaned_data.get('is_business_guest'):
        #     business = form_list[1].save()
        #     guest = guest_form.save(commit=False)
        #     guest.business = business
        #     guest.save()
        # else:
        #     guest = guest_form.save()

        # business = form_list[-1].save(commit=False)
        # booking.guest = guest
        # booking.save()

        # index = get_object_or_404(StudentIndexing, slug = indexing)

        # print ("index:", index)





class IndexingApplicationCreateView1(StaffRequiredMixin, SuccessMessageMixin,  CreateView):
    template_name = "students/start_indexing_application.html"
    utme_form = UtmeGradeModelForm
    student_indexing_form = StudentIndexingModelForm
    success_message = "%(student_profile)s Indexing Application Submission Successful"

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(IndexingApplicationCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            student_profile=self.object.student_profile.student.get_full_name,
        )

    def get(self, request, *args, **kwargs):
        utme_form = self.utme_form()
        student_indexing_form  = self.student_indexing_form()
        return render(request, self.template_name, {'utme_form':utme_form, 'student_indexing_form':student_indexing_form})

    
    def post(self, request, *args, **kwargs):
        student_indexing_form = self.student_indexing_form(request.POST, request.FILES)
        utme_form = self.utme_form(request.POST, request.FILES)

        if utme_form.is_valid() and student_indexing_form.is_valid():
            utme = utme_form.save()

            user = self.request.user
            student_profile = StudentProfile.objects.get(student=self.request.user)
            reg_no = user.reg_no
            institution = InstitutionProfile.objects.get(name= student_profile.institution)
            student = student_indexing_form.save(commit=False)
            indexing = StudentIndexing.objects.create(
                utme_grade = utme,
                student_profile = student_profile,
                academic_session = student.academic_session,
                admission_type = student.admission_type,
                institution = institution,
                reg_no = reg_no,
                )
            messages.success(request, "Indexing Application Submission Successful!")
            return redirect(indexing.get_absolute_url())
            
        print(request.POST)  
        messages.error(request, 'Form already submitted')
        return render(request, self.template_name, {'utme_form':utme_form, 'student_indexing_form':student_indexing_form})

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())

class IndexingPaymentCreateView(StaffRequiredMixin, SuccessMessageMixin,  CreateView):
    model = IndexingPayment
    template_name = "students/indexing_payment.html"
    form_class = IndexingPaymentModelForm


    def form_valid(self, form):
        payment = form.save(commit=False)
        user = self.request.user
        student_profile = StudentProfile.objects.get(student = user)
        matric_no = user.matric_no
        institution = InstitutionProfile.objects.get(name = student_profile.institution)
        student_indexing = StudentIndexing.objects.get(student_profile = student_profile)
        payment.institution = institution
        payment.student_indexing = student_indexing 
        payment.student_profile = student_profile
        payment.matric_no = matric_no
        payment.save()
        return super(IndexingPaymentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("students:my_indexing_payment_details", kwargs={"slug": self.object.slug})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)

    #     if form.is_valid():
    #         user = self.request.user
    #         student_profile = StudentProfile.objects.get(student=user)
    #         reg_no = user.reg_no
    #         institution = InstitutionProfile.objects.get(name= student_profile.institution)
    #         payment = form.save(commit=False)
    #         payment.institution = institution
    #         payment.student_profile = student_profile
    #         payment.reg_no = reg_no
    #         payment.save()

    #         return redirect(student.get_absolute_url())
      
    #     print(request.POST)  
    #     return render(request, self.template_name, {'form':form})


            





# class MyIndexingApplicationListView(LoginRequiredMixin, ListView):
#     template_name = "students/my_indexing_application_list.html"
#     def get_queryset(self):
#         request = self.request
#         qs = StudentProfile.objects.all()
#         query = request.GET.get('q')
#         user = self.request.user
#         if query:
#             qs = qs.filter(student__icontains=query)
#         return qs
        # if user.is_authenticated():
        #     qs = qs.owned(user)

class MyIndexingApplicationDetailView(StaffRequiredMixin, DetailView):
    # queryset = StudentIndexing.objects.all()
    template_name = "students/my_indexing_application_details.html"

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







class MyIndexingPaymentListView(StaffRequiredMixin, ListView):
    template_name = "students/my_indexing_payment_list.html"
    def get_queryset(self):
        request = self.request
        qs = IndexingPayment.objects.filter(student_profile__student=request.user)
        query = request.GET.get('q')
        if query:
            qs = qs.filter(student_profile__student__icontains=query)
        return qs 


class MyIndexingPaymentDetailView(StaffRequiredMixin, DetailView):
    queryset = IndexingPayment.objects.all()
    template_name = "students/my_indexing_payment_details.html"



class MyIndexingCompleteListView(StaffRequiredMixin, ListView):
    template_name = "students/my_indexing_complete_view.html"
    def get_queryset(self):
        request = self.request
        qs = IssueIndexing.objects.filter(student_profile__student = request.user)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(name__icontains=query)
        return qs 

    def get_context_data(self, **kwargs):
        context = super(MyIndexingCompleteListView, self).get_context_data(**kwargs)
        request = self.request
        st_profile = StudentProfile.objects.filter(student = request.user)
        student_profile = st_profile.first()
        institutions = InstitutionProfile.objects.filter(name = student_profile.institution)
        students = IssueIndexing.objects.filter(institution__in=institutions).filter(student_profile = student_profile)
        context = {
        'student_profile':student_profile,
        'institutions':institutions,
        'students':students,
        }
        return context
       



class MyIndexingNumberDetailView(StaffRequiredMixin, DetailView):
    queryset = IssueIndexing.objects.all()
    template_name = "students/my_indexing_number_details.html"






























# class IndexingApplicationCreateView(CreateView):
#     utme_form = UtmeGradeModelForm
#     student_indexing_form = StudentIndexingModelForm
#     template_name = 'students/student_indexing_application.html'

#     # def get_success_url(self):
#     #   return reverse("institutions:student_profile_details", kwargs={"slug": self.slug})
    
#     def get(self, request, *args, **kwargs):
#         utme_form = self.utme_form()
#         student_indexing_form  = self.student_indexing_form()
#         return render(request, self.template_name, {'utme_form':utme_form, 'student_indexing_form':student_indexing_form})

#     def post(self, request, *args, **kwargs):
#         utme_form = self.utme_form(request.POST)
#         student_indexing_form  = self.student_indexing_form(request.POST)

#         if utme_form.is_valid() and student_indexing_form .is_valid():
#             student_indexing_form.save(commit=False)
#             utme = utme_form.save()
#             # student = student_indexing_form.save(commit=False)
#             StudentIndexing.objects.create(
#                 student = user,
#                 course = student.course,
#                 institution = student.institution,
#                 reg_no = student.reg_no,               
#                 sex = student.sex,
#                 dob = student.dob,
#                 marital_status = student.marital_status,
#                 nationality = student.nationality,
#                 state_of_origin = student.state_of_origin,
#                 lga = student.lga,
#                 contact_address = student.contact_address,
#                 )

            



#             return redirect(student.get_absolute_url())
            
#             print(kwargs)
#             print('Hi')
#             print("kwargs: ", kwargs)
           
#         return render(request, self.template_name, {'user_form':user_form, 'student_form':student_form})



# class CourseListView(ListView):
#     paginate_by = 12

#     def get_context_data(self, *args, **kwargs):
#         context = super(CourseListView, self).get_context_data(*args, **kwargs)
#         print(dir(context.get('page_obj')))
#         return context

#     def get_queryset(self):
#         request = self.request
#         qs = Course.objects.all()
#         query = request.GET.get('q')
#         user = self.request.user
#         if query:
#             qs = qs.filter(title__icontains=query)
#         if user.is_authenticated():
        #     qs = qs.owned(user)
        # return qs 
