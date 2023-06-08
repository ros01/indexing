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
from .forms import *
from institutions.forms import *
from accounts.forms import SignupForm
from accounts.models import *
from .models import *
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

class DashboardView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwarg):
        user = self.request.user
        obj = StudentProfile.objects.filter(student=user)
        context = {
            "obj": obj,
        }

        return render(request, "students/dashboard1.html", context)

@login_required
def status(request):
    user = request.user
    if StudentProfile.objects.filter(student = user, indexing_status=1):
        return MyStudentProfileListView.as_view()(request)
    elif StudentProfile.objects.filter(student = user, indexing_status=2):
        return ApplicationList.as_view()(request)
    elif StudentIndexing.objects.filter(student_profile__student = user, indexing_status=2):
        return IndexingPaymentCreateListView.as_view()(request)
    elif StudentIndexing.objects.filter(student_profile__student = user, indexing_status=3):
        return MyIndexingApplicationListView.as_view()(request)
    else:
        return HttpResponseNotFound('404 Page not found')


class MyIndexingApplicationListView(LoginRequiredMixin, ListView):
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


class MyStudentProfileListView(LoginRequiredMixin, ListView):
    template_name = "students/my_student_profile_list.html"
    def get_queryset(self):
        request = self.request
        qs = StudentProfile.objects.filter(student=request.user)
        query = request.GET.get('q')
        user = self.request.user
        if query:
            qs = qs.filter(student__icontains=query)
        return qs


class ApplicationList(LoginRequiredMixin, ListView):
    template_name = "students/my_application_list.html"
    def get_queryset(self):
        request = self.request
        qs = StudentProfile.objects.filter(student=request.user)
        query = request.GET.get('q')
        user = self.request.user
        if query:
            qs = qs.filter(student__icontains=query)
        return qs

class IndexingPaymentCreateListView(LoginRequiredMixin, ListView):
    template_name = "students/my_indexing_payment_create_list.html"
    def get_queryset(self):
        request = self.request
        qs = StudentIndexing.objects.filter(student_profile__student=request.user)
        query = request.GET.get('q')
        if query:
            qs = qs.filter(student_profile__student__icontains=query)
        return qs 


class MyStudentProfileDetailView(LoginRequiredMixin, DetailView):
    queryset = StudentProfile.objects.all()
    template_name = "students/my_student_profile_details.html"



class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileModelForm
    template_name = "students/update_profile.html"


    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.indexing_status >2:
            pass
        else:
            instance.indexing_status = 2
        return super(UpdateProfile, self).form_valid(form)

    def get_success_url(self):
        return reverse("students:my_student_profile_details", kwargs={"slug": self.object.slug})



class IndexingApplicationCreateView(LoginRequiredMixin, CreateView):
    template_name = "students/start_indexing_application.html"
    utme_form = UtmeGradeModelForm
    student_indexing_form = StudentIndexingModelForm

    def get(self, request, *args, **kwargs):
        utme_form = self.utme_form()
        student_indexing_form  = self.student_indexing_form()
        return render(request, self.template_name, {'utme_form':utme_form, 'student_indexing_form':student_indexing_form})

    
    def post(self, request, *args, **kwargs):
        student_indexing_form = self.student_indexing_form(request.POST)
        utme_form = self.utme_form(request.POST)

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
            

            return redirect(indexing.get_absolute_url())
      
        print(request.POST)  
        return render(request, self.template_name, {'utme_form':utme_form, 'student_indexing_form':student_indexing_form})

class IndexingPaymentCreateView(LoginRequiredMixin, CreateView):
    model = IndexingPayment
    template_name = "students/indexing_payment.html"
    form_class = IndexingPaymentModelForm


    def form_valid(self, form):
        payment = form.save(commit=False)
        user = self.request.user
        student_profile = StudentProfile.objects.get(student = user)
        reg_no = user.reg_no
        institution = InstitutionProfile.objects.get(name = student_profile.institution)
        student_indexing = StudentIndexing.objects.get(student_profile = student_profile)
        payment.institution = institution
        payment.student_indexing = student_indexing 
        payment.student_profile = student_profile
        payment.reg_no = reg_no
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

class MyIndexingApplicationDetailView(LoginRequiredMixin, DetailView):
    queryset = StudentIndexing.objects.all()
    template_name = "students/my_indexing_application_details.html"


class MyIndexingPaymentListView(LoginRequiredMixin, ListView):
    template_name = "students/my_indexing_payment_list.html"
    def get_queryset(self):
        request = self.request
        qs = IndexingPayment.objects.filter(student_profile__student=request.user)
        query = request.GET.get('q')
        if query:
            qs = qs.filter(student_profile__student__icontains=query)
        return qs 


class MyIndexingPaymentDetailView(LoginRequiredMixin, DetailView):
    queryset = IndexingPayment.objects.all()
    template_name = "students/my_indexing_payment_details.html"

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
