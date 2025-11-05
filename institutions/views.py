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
from django.db import IntegrityError
from accounts.forms import *
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
from django.core.exceptions import ObjectDoesNotExist
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
from django.contrib.auth.decorators import login_required, user_passes_test
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
from django.views.decorators.csrf import csrf_exempt






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



# def staff_required(self, request, *args, **kwargs):
	
# 	if not request.user.role == 'Indexing Officer':
#             messages.error(
#                 request,
#                 ('You do not have the permission required to perform the '
#                 'requested operation.'))
#             return redirect(settings.LOGIN_URL)

# def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
#     '''
#     Decorator for views that checks that the logged in user is a teacher,
#     redirects to the log-in page if necessary.
#     '''
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.role == 'Indexing Officer',
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )            

def staff_required(function):
    def _function(request, *args, **kwargs):
        if request.user.role != 'Indexing Officer':
            messages.error(request, 'You do not have the permission required to perform the requested operation.')
            return HttpResponseRedirect(settings.LOGIN_URL)
        return _function


#@user_passes_test(staff_required)

        
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


class DashboardView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
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


class AdmissionQuotaListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
	template_name = "institutions/admission_quota_list.html"
	def get_queryset(self):
		request = self.request
		user = request.user
		qs = AdmissionQuota.objects.filter(institution = user.get_indexing_officer_profile.institution)
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs 

class AdmissionQuotaDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
	# queryset = AdmissionQuota.objects.all()
	template_name = "institutions/admission_quota_details.html"

	def get_object(self):
	    user = self.request.user
	    slug = self.kwargs.get("slug")  # from URL
	    return AdmissionQuota.objects.get(
	        institution=user.get_indexing_officer_profile.institution,
	        slug=slug
	    )

	# def get_object(self):
	# 	user = self.request.user
	# 	obj1 = AdmissionQuota.objects.filter(institution = user.get_indexing_officer_profile.institution)
	# 	obj = obj1.first()
	# 	return obj

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


@login_required
def slug_router(request, slug):
    if InstitutionProfile.objects.filter(slug=slug).exists():
        return StudentProfilesListView.as_view()(request, slug=slug)
    elif InstitutionProfile.objects.filter(slug=slug).exists():
        return DashboardView.as_view()(request, slug=slug)
    else:
        return HttpResponseNotFound('404 Page not found')    

@login_required
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

# class CreateAcademicSession(StaffRequiredMixin, CreateView):
#     template_name = 'store/create_vendor2.html'
#     form_class = AcademicSessionModelForm
#     success_message = 'Academic Session created Successfully.'


class InstitutionObjectMixin(object):
    model = InstitutionProfile
    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(self.model, slug=slug)
        return obj 



@login_required
def batch_create_student_profiles(request):
	academic_sessions = AcademicSession.objects.filter(status = 1)
	academic_session = request.GET.get('academic_session') or None
	# print("Academic Session S:", academic_session)
	form = StudentProfileModelForm(request.POST or None)
	context = {'academic_sessions': academic_sessions, 'academic_session': academic_session, 'form':form, 'is_htmx': True}
	# return render(request, 'institutions/pay_institutions_indexing_fee.html', context)
	# return render(request, 'institutions/bulk_create_students.html', context)
	return render(request, 'institutions/bulk_upload_students.html', context)

@method_decorator(csrf_exempt, name='dispatch')
class PreviewStudentCSV(View):
    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('students_list')
            if not file:
                return HttpResponse("No file uploaded", status=400)
            
            paramFile = io.TextIOWrapper(file.file, encoding='utf-8')
            reader = csv.DictReader(paramFile)
            data = list(reader)

            if not data:
                return HttpResponse("CSV is empty", status=400)

            html = render_to_string("partials/_students_csv_preview.html", {"students": data})
            return HttpResponse(html)

        except Exception as e:
            return HttpResponse(f"Error processing CSV: {str(e)}", status=500)

class StudentProfileCreateView0(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, CreateView):
	form = StudentProfileModelForm
	def get(self, request, *args, **kwargs):
		form = StudentProfileModelForm()
		template_name = 'partials/bulk_create_students.html'

		user = self.request.user
		institution = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution).first()
		# print("Institution1:", institution)
		session = self.request.GET.get('academic_session')
		# print("Form Session:", session)
		academic_session_name = AcademicSession.objects.get(id=session)
		# print("Academic Session1:", academic_session_name)
		academic_session = academic_session_name.id
		quota = AdmissionQuota.objects.get_or_none(institution = institution, academic_session = academic_session)
		admission_quota = quota.admission_quota
		students_list = StudentProfile.objects.filter(institution = institution, academic_session = academic_session)
		quota_used = len(students_list)
		quota_remaining = admission_quota - quota_used
		context = { 'quota_remaining': quota_remaining, 'quota_used': quota_used, 'admission_quota': admission_quota, 'academic_session': academic_session, 'academic_session_name': academic_session_name, 'form':form}
		# print("A Quota:", quota.admission_quota)
		if quota.status == 0:
			messages.error(self.request, "This session is locked for students indexing. Please select an active academic session to proceed or Contact RRBN")
			return redirect("institutions:batch_create_student_profiles")
		else:
			return render(request, template_name, context)

	def get_form(self, *args, **kwargs):
		form = super(StudentProfileCreateView, self).get_form(*args, **kwargs)
		academic_session = self.get_academic_session()
		form.fields["academic_session"].queryset = academic_session
		return form

			
	def post(self, request, *args, **kwargs):
		user = self.request.user
		institution = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution).first()
		# print("Institution:", institution)
		session = request.POST.get('academic_session')
		academic_session = AcademicSession.objects.get(id=session)
		# print("Academic Session:", academic_session)
		quota = AdmissionQuota.objects.get_or_none(institution = institution, academic_session = academic_session)
		# print("Quota:", quota)
		if quota is None:
			admission_quota = 0;
		else:
			admission_quota = quota.admission_quota
		# print("Admission Quota:", admission_quota)
		students_qs = institution.studentprofile_set.all()		

		students_list = students_qs.filter(academic_session = academic_session)
		paramFile = io.TextIOWrapper(request.FILES['students_list'].file)
		portfolio1 = csv.DictReader(paramFile)
		list_of_dict = list(portfolio1)
		email_check = list_of_dict[0]["email"] == None

		try:
			context = {}
			if len(list_of_dict) == 0:
				messages.error(request, "No Data in List. Please populate list and try again")
				# print("Number in List:",  len(list_of_dict))
				return redirect("institutions:batch_create_student_profiles")
			elif email_check:
				messages.error(request, "No email in list. Please add email and try again")
				# print("Number of emails in List:",  len(data[0]["email"]))
				return redirect("institutions:batch_create_student_profiles")
			elif admission_quota == 0:
				messages.error(request, "No Quota Assigned for Selected Academic Session")
				# print("Number in List:",  len(list_of_dict))
				# print("Number of students registered:", len(students_list))
				# print("Admission Quota:", int(admission_quota))
				return redirect("institutions:batch_create_student_profiles")

			elif len(students_list) > admission_quota or len(list_of_dict) > admission_quota or len(list_of_dict) + int(len(students_list)) > admission_quota:
				messages.error(request, "Admission Quota exceeded!")
				# print("Number in List:",  len(list_of_dict))
				# print("Number of students registered:", len(students_list))
				# print("Admission Quotas:", int(admission_quota))
				return redirect("institutions:batch_create_student_profiles")
			else:
				for row in list_of_dict:
					data = row['email']
					students_list = User.objects.filter(email=data)
					try:
						if students_list.exists():
							messages.error(request, f'This User: {data} and possibly other students on this list exit already exist')
							return redirect("institutions:batch_create_student_profiles")
						else:
							data = [(
							User.objects.create(email=row['email'], last_name=row['last_name'], first_name=row['first_name'], middle_name=row['middle_name'], phone_no=row['phone_no'], matric_no=row['matric_no'], password = make_password('student@001'),))
							for row in list_of_dict]

							objs = [
					            StudentProfile(
					            	student = User.objects.get(email=row['email']),
					            	institution=institution,
					            	academic_session = academic_session,
					            )
					            for row in list_of_dict]
							for obj in objs:
								obj.slug = create_slug3(instance=obj)
								user = obj.student
								reset_password(user, request)
							
							nmsg = StudentProfile.objects.bulk_create(objs)
							messages.success(request, "Bulk Create of Students successful!")
							returnmsg = {"status_code": 200}
							return redirect("institutions:batch_create_student_profiles")
					except Exception as e:
						messages.error(request, e)
						return redirect("institutions:batch_create_student_profiles")				
		except Exception as e:
			print('Error While Importing Data: ', e)
			returnmsg = {"status_code": 500}
			return JsonResponse(returnmsg)
			return redirect("institutions:batch_create_student_profiles")
		
def generate_user_slug(row):
    base = f"{row['first_name']}-{row['last_name']}-{row['email'].split('@')[0]}"
    return slugify(base) + "-" + uuid.uuid4().hex[:4] 


class StudentProfileCreateView(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, CreateView):
    form = StudentProfileModelForm
    template_name = 'partials/bulk_upload_students.html'

    def get(self, request, *args, **kwargs):
        form = self.form()
        session_id = request.GET.get('academic_session')
        if not session_id:
            messages.error(request, "Academic session not provided.")
            return redirect("institutions:batch_create_student_profiles")

        academic_session = get_object_or_404(AcademicSession, id=session_id)
        user = request.user
        institution = user.get_indexing_officer_profile.institution
        quota = AdmissionQuota.objects.get_or_none(institution=institution, academic_session=academic_session)

        if not quota:
            messages.error(request, "No admission quota set for this session.")
            return redirect("institutions:batch_create_student_profiles")

        if quota.status == 0:
            messages.error(request, "This session is locked for indexing. Contact RRBN.")
            return redirect("institutions:batch_create_student_profiles")

        students_list = StudentProfile.objects.filter(institution=institution, academic_session=academic_session)
        context = {
            'form': form,
            'academic_session': academic_session.id,
            'academic_session_name': academic_session,
            'quota_remaining': quota.admission_quota - students_list.count(),
            'quota_used': students_list.count(),
            'admission_quota': quota.admission_quota,
        }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
	    import logging
	    logger = logging.getLogger(__name__)

	    action = request.POST.get("action_type", "create")
	    file = request.FILES.get("students_list")

	    if not file:
	        messages.error(request, "No file uploaded.")
	        return redirect("institutions:batch_create_student_profiles")

	    try:
	        decoded_file = io.TextIOWrapper(file.file, encoding='utf-8')
	        reader = csv.DictReader(decoded_file)
	        data = list(reader)
	    except Exception as e:
	        logger.exception("Failed to decode or read CSV")
	        messages.error(request, f"Invalid CSV format: {str(e)}")
	        return redirect("institutions:batch_create_student_profiles")

	    if not data:
	        messages.error(request, "CSV file is empty.")
	        return redirect("institutions:batch_create_student_profiles")

	    required_fields = {"email", "last_name", "first_name", "middle_name", "phone_no", "matric_no"}
	    if not required_fields.issubset(data[0]):
	        messages.error(request, "CSV headers missing required fields.")
	        return redirect("institutions:batch_create_student_profiles")

	    session_id = request.POST.get('academic_session')
	    academic_session = get_object_or_404(AcademicSession, id=session_id)
	    user = request.user
	    institution = user.get_indexing_officer_profile.institution
	    quota = AdmissionQuota.objects.get_or_none(institution=institution, academic_session=academic_session)
	    admission_quota = quota.admission_quota if quota else 0

	    existing_students_count = StudentProfile.objects.filter(institution=institution, academic_session=academic_session).count()
	    if len(data) + existing_students_count > admission_quota:
	        messages.error(request, "Admission quota exceeded.")
	        return redirect("institutions:batch_create_student_profiles")

	    if action == "preview":
	        context = {"students": data}
	        return render(request, "partials/preview_table.html", context)

	    emails = [row['email'] for row in data]
	    existing_users = User.objects.filter(email__in=emails).values_list('email', flat=True)
	    duplicate_emails = set(emails) & set(existing_users)

	    if duplicate_emails:
	        messages.error(request, f"Duplicate emails found: {', '.join(duplicate_emails)}")
	        return redirect("institutions:batch_create_student_profiles")

	    try:
	        with transaction.atomic():
	            # Create Users
	            new_users = []
	            for row in data:
	                user = User(
	                    email=row['email'],
	                    first_name=row['first_name'],
	                    last_name=row['last_name'],
	                    middle_name=row['middle_name'],
	                    phone_no=row['phone_no'],
	                    matric_no=row['matric_no'],
	                    password=make_password("student@001"),
	                    slug=slugify(row['email'])  # TEMP fix
	                )
	                new_users.append(user)

	            logger.info(f"Creating {len(new_users)} users...")
	            User.objects.bulk_create(new_users, batch_size=1000)

	            # Verify creation
	            created_users = list(User.objects.filter(email__in=emails))
	            user_map = {u.email: u for u in created_users}
	            logger.info(f"Successfully created {len(created_users)} users.")
	            new_profiles = [
				    StudentProfile(
				        student=user_map[row['email']],
				        institution=institution,
				        academic_session=academic_session,
				        slug=create_slug3_from_user(user_map[row['email']])
				    )
				    for row in data
				]

	            # Create StudentProfiles
	            # new_profiles = []
	            # for row in data:
	            #     user = user_map.get(row['email'])
	            #     if user:
	            #         profile = StudentProfile(
	            #             student=user,
	            #             institution=institution,
	            #             academic_session=academic_session,
	            #             slug=create_slug3(user)
	            #         )
	            #         new_profiles.append(profile)

	            StudentProfile.objects.bulk_create(new_profiles, batch_size=1000)
	            logger.info(f"Successfully created {len(new_profiles)} student profiles.")

	            # Now reset passwords correctly
	            for user in user_map.values():
	                reset_password(user, request)

	    except Exception as e:
	        logger.exception("Error during batch creation.")
	        messages.error(request, f"An error occurred during upload: {str(e)}")
	        return redirect("institutions:batch_create_student_profiles")

	    messages.success(request, "Students uploaded successfully.")
	    return redirect("institutions:batch_create_student_profiles")



    # def post(self, request, *args, **kwargs):
	#     action = request.POST.get("action_type", "create")
	#     file = request.FILES.get("students_list")

	#     if not file:
	#         messages.error(request, "No file uploaded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     try:
	#         decoded_file = io.TextIOWrapper(file.file, encoding='utf-8')
	#         reader = csv.DictReader(decoded_file)
	#         data = list(reader)
	#     except Exception:
	#         messages.error(request, "Invalid CSV format.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     if not data:
	#         messages.error(request, "CSV file is empty.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     required_fields = {"email", "last_name", "first_name", "middle_name", "phone_no", "matric_no"}
	#     if not required_fields.issubset(data[0]):
	#         messages.error(request, "CSV headers missing required fields.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     session_id = request.POST.get('academic_session')
	#     academic_session = get_object_or_404(AcademicSession, id=session_id)
	#     user = request.user
	#     institution = user.get_indexing_officer_profile.institution
	#     quota = AdmissionQuota.objects.get_or_none(institution=institution, academic_session=academic_session)
	#     admission_quota = quota.admission_quota if quota else 0

	#     existing_students_count = StudentProfile.objects.filter(institution=institution, academic_session=academic_session).count()
	#     if len(data) + existing_students_count > admission_quota:
	#         messages.error(request, "Admission quota exceeded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     if action == "preview":
	#         context = {"students": data}
	#         return render(request, "partials/preview_table.html", context)

	#     emails = [row['email'] for row in data]
	#     existing_emails = set(User.objects.filter(email__in=emails).values_list('email', flat=True))
	#     duplicate_emails = set(emails) & existing_emails

	#     if duplicate_emails:
	#         messages.error(request, f"Duplicate emails found: {', '.join(duplicate_emails)}")
	#         return redirect("institutions:batch_create_student_profiles")

	#     try:
	#     	with transaction.atomic():
	# 		    new_users = []
	# 		    for row in data:
	# 		        try:
	# 		            user = User(
	# 		                email=row['email'],
	# 		                first_name=row['first_name'],
	# 		                last_name=row['last_name'],
	# 		                middle_name=row['middle_name'],
	# 		                phone_no=row['phone_no'],
	# 		                matric_no=row['matric_no'],
	# 		                password=make_password("student@001"),
	# 		                slug=slugify(row['email']),  # TEMP: test with simple slug
	# 		            )
	# 		            new_users.append(user)
	# 		        except Exception as e:
	# 		            print(f"Error building user: {e}")

	# 		    print("Creating", len(new_users), "users...")
	# 		    User.objects.bulk_create(new_users, batch_size=1000)

	# 		    created_users = User.objects.filter(email__in=[u.email for u in new_users])
	# 		    print("Created in DB:", created_users.count())
	# 		    user_map = {u.email: u for u in created_users}

	# 		    new_profiles = []
	# 		    for row in data:
	# 		        user = user_map.get(row['email'])
	# 		        if user:
	# 		            profile = StudentProfile(
	# 		                student=user,
	# 		                institution=institution,
	# 		                academic_session=academic_session,
	# 		                slug=create_slug3(user),
	# 		            )
	# 		            new_profiles.append(profile)

	# 		    StudentProfile.objects.bulk_create(new_profiles, batch_size=1000)
	# 		    print("Created", len(new_profiles), "student profiles")

	# 		    for user in user_map.values():
	# 		        reset_password(user, request)

	    	# with transaction.atomic():
	    	# 	print("Total rows from CSV:", len(data))
			# 	print("First row:", data[0])

			#     new_users = []
			#     for row in data:
			#         if row['email'] not in existing_emails:
			#             try:
			#                 user = User(
			#                     email=row['email'],
			#                     first_name=row['first_name'],
			#                     last_name=row['last_name'],
			#                     middle_name=row['middle_name'],
			#                     phone_no=row['phone_no'],
			#                     matric_no=row['matric_no'],
			#                     password=make_password("student@001"),
			#                     slug=generate_user_slug(row),
			#                 )
			#                 new_users.append(user)
			#             except Exception as e:
			#                 print(f"Skipping user due to error: {e}")

			#     User.objects.bulk_create(new_users, batch_size=1000)
			#     print("Bulk user creation done.")
			#     print("Created users in DB:", User.objects.filter(email__in=[u.email for u in new_users]).count())


			#     # Re-fetch to get DB instances
			#     created_users = User.objects.filter(email__in=[u.email for u in new_users])
			#     user_map = {u.email: u for u in created_users}

			#     print(f"Created {len(user_map)} users")

			#     new_profiles = []
			#     for row in data:
			#         user = user_map.get(row['email'])
			#         if user:
			#             new_profiles.append(
			#                 StudentProfile(
			#                     student=user,
			#                     institution=institution,
			#                     academic_session=academic_session,
			#                     slug=create_slug3(user)
			#                 )
			#             )

			#     StudentProfile.objects.bulk_create(new_profiles, batch_size=1000)

			#     for user in user_map.values():
			#         reset_password(user, request)

	        # with transaction.atomic():
	        #     new_users_data = [row for row in data if row['email'] not in existing_emails]

	        #     new_users = [
	        #         User(
	        #             email=row['email'],
	        #             first_name=row['first_name'],
	        #             last_name=row['last_name'],
	        #             middle_name=row['middle_name'],
	        #             phone_no=row['phone_no'],
	        #             matric_no=row['matric_no'],
	        #             password=make_password("student@001"),
	        #             slug=generate_user_slug(row),
	        #         )
	        #         for row in new_users_data
	        #     ]

	        #     User.objects.bulk_create(new_users, batch_size=1000)

	        #     # Confirm that users were actually created
	        #     created_users = User.objects.filter(email__in=[row['email'] for row in new_users_data])
	        #     user_map = {user.email: user for user in created_users}

	        #     if not created_users:
	        #         messages.error(request, "No users were created. Check for issues in data or creation logic.")
	        #         return redirect("institutions:batch_create_student_profiles")

	        #     new_profiles = [
	        #         StudentProfile(
	        #             student=user_map[row['email']],
	        #             institution=institution,
	        #             academic_session=academic_session,
	        #             slug=create_slug3(user_map[row['email']])
	        #         )
	        #         for row in new_users_data if row['email'] in user_map
	        #     ]

	        #     StudentProfile.objects.bulk_create(new_profiles, batch_size=1000)

	        #     for profile in new_profiles:
	        #         reset_password(profile.student, request)

	    # except Exception as e:
	    #     messages.error(request, f"An error occurred during upload: {str(e)}")
	    #     return redirect("institutions:batch_create_student_profiles")

	    # messages.success(request, "Students uploaded successfully.")
	    # return redirect("institutions:batch_create_student_profiles")


    # def post(self, request, *args, **kwargs):
	#     action = request.POST.get("action_type", "create")
	#     file = request.FILES.get("students_list")

	#     if not file:
	#         messages.error(request, "No file uploaded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     try:
	#         decoded_file = io.TextIOWrapper(file.file, encoding='utf-8')
	#         reader = csv.DictReader(decoded_file)
	#         data = list(reader)
	#     except Exception:
	#         messages.error(request, "Invalid CSV format.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     if not data:
	#         messages.error(request, "CSV file is empty.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     required_fields = {"email", "last_name", "first_name", "middle_name", "phone_no", "matric_no"}
	#     if not required_fields.issubset(data[0]):
	#         messages.error(request, "CSV headers missing required fields.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     session_id = request.POST.get('academic_session')
	#     academic_session = get_object_or_404(AcademicSession, id=session_id)
	#     user = request.user
	#     institution = user.get_indexing_officer_profile.institution
	#     quota = AdmissionQuota.objects.get_or_none(institution=institution, academic_session=academic_session)
	#     admission_quota = quota.admission_quota if quota else 0

	#     existing_students_count = StudentProfile.objects.filter(
	#         institution=institution, academic_session=academic_session
	#     ).count()

	#     if len(data) + existing_students_count > admission_quota:
	#         messages.error(request, "Admission quota exceeded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     if action == "preview":
	#         # Render preview table
	#         context = {
	#             "students": data
	#         }
	#         return render(request, "partials/preview_table.html", context)

	#     emails = [row['email'] for row in data]
	#     existing_users = User.objects.filter(email__in=emails).values_list('email', flat=True)
	#     duplicate_emails = set(emails) & set(existing_users)

	#     if duplicate_emails:
	#         messages.error(request, f"Duplicate emails found: {', '.join(duplicate_emails)}")
	#         return redirect("institutions:batch_create_student_profiles")

	#     try:
	#         with transaction.atomic():
	#             # Create users with slugs
	#             new_users = [
	#                 User(
	#                     email=row['email'],
	#                     first_name=row['first_name'],
	#                     last_name=row['last_name'],
	#                     middle_name=row['middle_name'],
	#                     phone_no=row['phone_no'],
	#                     matric_no=row['matric_no'],
	#                     password=make_password("student@001"),
	#                     slug=generate_user_slug(row),
	#                 )
	#                 for row in data
	#             ]
	#             User.objects.bulk_create(new_users, batch_size=1000)

	#             created_users = User.objects.filter(email__in=emails)
	#             user_map = {user.email: user for user in created_users}

	#             new_profiles = [
	#                 StudentProfile(
	#                     student=user_map[row['email']],
	#                     institution=institution,
	#                     academic_session=academic_session,
	#                     slug=create_slug3(user_map[row['email']])  # Assuming create_slug3 accepts instance
	#                 )
	#                 for row in data
	#             ]
	#             StudentProfile.objects.bulk_create(new_profiles, batch_size=1000)
	#             saved_profiles = StudentProfile.objects.select_related('student').filter(
	# 			    student__email__in=emails,
	# 			    institution=institution,
	# 			    academic_session=academic_session,
	# 			)
	# 			# for profile in saved_profiles:
	# 			#     reset_password(profile.student, request)


	#             for profile in saved_profiles:
	#                 reset_password(profile.student, request)

	#     except Exception as e:
	#         messages.error(request, f"An error occurred during upload: {str(e)}")
	#         return redirect("institutions:batch_create_student_profiles")

	#     messages.success(request, "Students uploaded successfully.")
	#     return redirect("institutions:batch_create_student_profiles")


    # def post(self, request, *args, **kwargs):
    # 	action = request.POST.get("action_type", "create")
    # 	file = request.FILES.get("students_list")
    # 	if not file:
    #         messages.error(request, "No file uploaded.")
    #         return redirect("institutions:batch_create_student_profiles")
    #     try:
    #         decoded_file = io.TextIOWrapper(file.file, encoding='utf-8')
    #         reader = csv.DictReader(decoded_file)
    #         data = list(reader)
    #     except Exception:
    #         messages.error(request, "Invalid CSV format.")
    #         return redirect("institutions:batch_create_student_profiles")

    #     if not data:
    #         messages.error(request, "CSV file is empty.")
    #         return redirect("institutions:batch_create_student_profiles")

    #     required_fields = {"email", "last_name", "first_name", "middle_name", "phone_no", "matric_no"}
    #     if not required_fields.issubset(data[0]):
    #         messages.error(request, "CSV headers missing required fields.")
    #         return redirect("institutions:batch_create_student_profiles")

    #     session_id = request.POST.get('academic_session')
    #     academic_session = get_object_or_404(AcademicSession, id=session_id)
    #     user = request.user
    #     institution = user.get_indexing_officer_profile.institution
    #     quota = AdmissionQuota.objects.get_or_none(institution=institution, academic_session=academic_session)
    #     admission_quota = quota.admission_quota if quota else 0

    #     existing_students_count = StudentProfile.objects.filter(institution=institution, academic_session=academic_session).count()
    #     if len(data) + existing_students_count > admission_quota:
    #         messages.error(request, "Admission quota exceeded.")
    #         return redirect("institutions:batch_create_student_profiles")

    #     if action == "preview":
	#         # Render preview table (you can style this in 'partials/preview_table.html')
	#         context = {
	#             "students": data
	#         }
	#         return render(request, "partials/preview_table.html", context)

    #     emails = [row['email'] for row in data]
    #     existing_users = User.objects.filter(email__in=emails).values_list('email', flat=True)
    #     duplicate_emails = set(emails) & set(existing_users)

    #     if duplicate_emails:
    #         messages.error(request, f"Duplicate emails found: {', '.join(duplicate_emails)}")
    #         return redirect("institutions:batch_create_student_profiles")

    #     try:
    #         with transaction.atomic():
    #             # Create users with slugs
    #             new_users = [
    #                 User(
    #                     email=row['email'],
    #                     first_name=row['first_name'],
    #                     last_name=row['last_name'],
    #                     middle_name=row['middle_name'],
    #                     phone_no=row['phone_no'],
    #                     matric_no=row['matric_no'],
    #                     password=make_password("student@001"),
    #                     slug=generate_user_slug(row),
    #                 )
    #                 for row in data
    #             ]
    #             User.objects.bulk_create(new_users, batch_size=1000)

    #             # Create student profiles
    #             created_users = User.objects.filter(email__in=emails)
    #             user_map = {user.email: user for user in created_users}

    #             new_profiles = [
    #                 StudentProfile(
    #                     student=user_map[row['email']],
    #                     institution=institution,
    #                     academic_session=academic_session,
    #                     slug=create_slug3(user_map[row['email']])  # Assuming create_slug3 accepts instance
    #                 )
    #                 for row in data
    #             ]
    #             StudentProfile.objects.bulk_create(new_profiles, batch_size=1000)

               
    #             for profile in new_profiles:
    #                 reset_password(profile.student, request)

    #     except Exception as e:
    #         messages.error(request, f"An error occurred during upload: {str(e)}")
    #         return redirect("institutions:batch_create_student_profiles")

    #     messages.success(request, "Students uploaded successfully.")
    #     return redirect("institutions:batch_create_student_profiles")



    # def post(self, request, *args, **kwargs):
	#     action = request.POST.get("action_type", "create")
	#     file = request.FILES.get("students_list")
	#     if not file:
	#         messages.error(request, "No file uploaded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     try:
	#         decoded_file = io.TextIOWrapper(file.file, encoding='utf-8')
	#         reader = csv.DictReader(decoded_file)
	#         data = list(reader)
	#     except Exception:
	#         messages.error(request, "Invalid CSV format.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     if not data:
	#         messages.error(request, "CSV file is empty.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     required_fields = {"email", "last_name", "first_name", "middle_name", "phone_no", "matric_no"}
	#     if not required_fields.issubset(data[0]):
	#         messages.error(request, "CSV headers missing required fields.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     session_id = request.POST.get("academic_session")
	#     academic_session = get_object_or_404(AcademicSession, id=session_id)
	#     user = request.user
	#     institution = user.get_indexing_officer_profile.institution
	#     quota = AdmissionQuota.objects.get_or_none(institution=institution, academic_session=academic_session)
	#     admission_quota = quota.admission_quota if quota else 0

	#     existing_students_count = StudentProfile.objects.filter(institution=institution, academic_session=academic_session).count()
	#     if len(data) + existing_students_count > admission_quota:
	#         messages.error(request, "Admission quota exceeded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     if action == "preview":
	#         # Render preview table (you can style this in 'partials/preview_table.html')
	#         context = {
	#             "students": data
	#         }
	#         return render(request, "partials/preview_table.html", context)

	#     # Create action
	#     emails = [row['email'] for row in data]
	#     existing_users = User.objects.filter(email__in=emails).values_list('email', flat=True)
	#     duplicate_emails = set(emails) & set(existing_users)

	#     if duplicate_emails:
	#         messages.error(request, f"Duplicate emails found: {', '.join(duplicate_emails)}")
	#         return redirect("institutions:batch_create_student_profiles")

	#     new_users = [
	# 	    User(
	# 	        email=row['email'],
	# 	        first_name=row['first_name'],
	# 	        last_name=row['last_name'],
	# 	        middle_name=row['middle_name'],
	# 	        phone_no=row['phone_no'],
	# 	        matric_no=row['matric_no'],
	# 	        password=make_password("student@001"),
	# 	        slug=create_slug0_stub(row)  # your custom slug function
	# 	    )
	# 	    for row in data
	# 	]

	#     User.objects.bulk_create(new_users)

	#     user_map = {u.email: u for u in User.objects.filter(email__in=emails)}

	#     new_profiles = [
	#         StudentProfile(
	#             student=user_map[row['email']],
	#             institution=institution,
	#             academic_session=academic_session,
	#         )
	#         for row in data
	#     ]
	#     for profile in new_profiles:
	#         profile.slug = create_slug3(profile)

	#     StudentProfile.objects.bulk_create(new_profiles)

	#     for profile in new_profiles:
	#         reset_password(profile.student, request)

	#     messages.success(request, "Students uploaded successfully.")
	#     return redirect("institutions:batch_create_student_profiles")


    # def post(self, request, *args, **kwargs):
	#     action = request.POST.get("action_type", "create")
	#     file = request.FILES.get("students_list")
	#     if not file:
	#         messages.error(request, "No file uploaded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     try:
	#         decoded_file = io.TextIOWrapper(file.file, encoding='utf-8')
	#         reader = csv.DictReader(decoded_file)
	#         data = list(reader)
	#     except Exception:
	#         messages.error(request, "Invalid CSV format.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     if not data:
	#         messages.error(request, "CSV file is empty.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     required_fields = {"email", "last_name", "first_name", "middle_name", "phone_no", "matric_no"}
	#     if not required_fields.issubset(data[0]):
	#         messages.error(request, "CSV headers missing required fields.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     session_id = request.POST.get("academic_session")
	#     academic_session = get_object_or_404(AcademicSession, id=session_id)
	#     user = request.user
	#     institution = user.get_indexing_officer_profile.institution
	#     quota = AdmissionQuota.objects.get_or_none(institution=institution, academic_session=academic_session)
	#     admission_quota = quota.admission_quota if quota else 0

	#     existing_students_count = StudentProfile.objects.filter(institution=institution, academic_session=academic_session).count()
	#     if len(data) + existing_students_count > admission_quota:
	#         messages.error(request, "Admission quota exceeded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     if action == "preview":
	#         # Render preview table (you can style this in 'partials/preview_table.html')
	#         context = {
	#             "students": data
	#         }
	#         return render(request, "partials/preview_table.html", context)

	#     # Create action
	#     emails = [row['email'] for row in data]
	#     existing_users = User.objects.filter(email__in=emails).values_list('email', flat=True)
	#     duplicate_emails = set(emails) & set(existing_users)

	#     if duplicate_emails:
	#         messages.error(request, f"Duplicate emails found: {', '.join(duplicate_emails)}")
	#         return redirect("institutions:batch_create_student_profiles")

	#     new_users = [
	#         User(
	#             email=row['email'],
	#             first_name=row['first_name'],
	#             last_name=row['last_name'],
	#             middle_name=row['middle_name'],
	#             phone_no=row['phone_no'],
	#             matric_no=row['matric_no'],
	#             password=make_password("student@001"),
	#         )
	#         for row in data
	#     ]
	#     User.objects.bulk_create(new_users)

	#     user_map = {u.email: u for u in User.objects.filter(email__in=emails)}

	#     new_profiles = [
	#         StudentProfile(
	#             student=user_map[row['email']],
	#             institution=institution,
	#             academic_session=academic_session,
	#         )
	#         for row in data
	#     ]
	#     for profile in new_profiles:
	#         profile.slug = create_slug3(profile)

	#     StudentProfile.objects.bulk_create(new_profiles)

	#     for profile in new_profiles:
	#         reset_password(profile.student, request)

	#     messages.success(request, "Students uploaded successfully.")
	#     return redirect("institutions:batch_create_student_profiles")

    # def post(self, request, *args, **kwargs):
	#     print("FILES:", request.FILES)
	#     print("POST:", request.POST)

	#     file = request.FILES.get("students_list")
	#     if not file:
	#         messages.error(request, "No file uploaded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     try:
	#         decoded_file = io.TextIOWrapper(file.file, encoding='utf-8')
	#         reader = csv.DictReader(decoded_file)
	#         data = list(reader)
	#     except Exception:
	#         messages.error(request, "Invalid CSV format.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     if not data:
	#         messages.error(request, "CSV file is empty.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     required_fields = {"email", "last_name", "first_name", "middle_name", "phone_no", "matric_no"}
	#     if not required_fields.issubset(data[0]):
	#         messages.error(request, "CSV headers missing required fields.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     session_id = request.POST.get('academic_session')
	#     academic_session = get_object_or_404(AcademicSession, id=session_id)
	#     user = request.user
	#     institution = user.get_indexing_officer_profile.institution
	#     quota = AdmissionQuota.objects.get_or_none(institution=institution, academic_session=academic_session)
	#     admission_quota = quota.admission_quota if quota else 0

	#     existing_students_count = StudentProfile.objects.filter(institution=institution, academic_session=academic_session).count()
	#     if len(data) + existing_students_count > admission_quota:
	#         messages.error(request, "Admission quota exceeded.")
	#         return redirect("institutions:batch_create_student_profiles")

	#     emails = [row['email'] for row in data]
	#     existing_users = User.objects.filter(email__in=emails).values_list('email', flat=True)
	#     duplicate_emails = set(emails) & set(existing_users)

	#     if duplicate_emails:
	#         messages.error(request, f"Duplicate emails found: {', '.join(duplicate_emails)}")
	#         return redirect("institutions:batch_create_student_profiles")

	#     new_users = [
	#         User(
	#             email=row['email'],
	#             first_name=row['first_name'],
	#             last_name=row['last_name'],
	#             middle_name=row['middle_name'],
	#             phone_no=row['phone_no'],
	#             matric_no=row['matric_no'],
	#             password=make_password("student@001"),
	#         )
	#         for row in data
	#     ]
	#     User.objects.bulk_create(new_users)

	#     user_map = {u.email: u for u in User.objects.filter(email__in=emails)}

	#     new_profiles = [
	#         StudentProfile(
	#             student=user_map[row['email']],
	#             institution=institution,
	#             academic_session=academic_session,
	#         )
	#         for row in data
	#     ]

	#     for profile in new_profiles:
	#         profile.slug = create_slug3(profile)

	#     StudentProfile.objects.bulk_create(new_profiles)

	#     for profile in new_profiles:
	#         reset_password(profile.student, request)

	#     messages.success(request, "Students uploaded successfully.")
	#     return redirect("institutions:batch_create_student_profiles")



class StudentProfileCreateView1(StaffRequiredMixin, SuccessMessageMixin, CreateView):
	form = StudentProfileModelForm
	def get(self, request, *args, **kwargs):
		form = StudentProfileModelForm()
		template_name = 'partials/bulk_create_students.html'

		user = self.request.user
		# form = StudentProfileModelForm()
		institution = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution).first()
		print("Institution1:", institution)
		session = self.request.GET.get('academic_session')
		# session = form['academic_session'].value()
		print("Form Session:", session)
		academic_session_name = AcademicSession.objects.get(id=session)
		print("Academic Session1:", academic_session_name)
		academic_session = academic_session_name.id
		quota = AdmissionQuota.objects.get_or_none(institution = institution, academic_session = academic_session)
		admission_quota = quota.admission_quota
		students_list = StudentProfile.objects.filter(institution = institution, academic_session = academic_session)
		quota_used = len(students_list)
		quota_remaining = admission_quota - quota_used
		context = { 'quota_remaining': quota_remaining, 'quota_used': quota_used, 'admission_quota': admission_quota, 'academic_session': academic_session, 'academic_session_name': academic_session_name, 'form':form}
		print("A Quota:", quota.admission_quota)
		if quota.status == 0:
			messages.error(self.request, "This session is locked for students indexing. Please select an active academic session to proceed ")
			return redirect("institutions:batch_create_student_profiles")
		else:
			return render(request, template_name, context)

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['academic_sessions'] = AcademicSession.objects.all()
	# 	context['academic_session'] = self.request.GET.get('academic_session')
	# 	context['is_htmx'] = True
	# 	return context

	# def get_context_data(self, request, *args, **kwarg):
	# 	user = self.request.user
	# 	form = StudentProfileModelForm()
	# 	qs1 = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
	# 	obj = qs1.first().studentprofile_set.all()
	# 	context['object'] = obj
	# 	context['form'] = form

	# def dispatch(self, *args, **kwargs):
	# 	# quota = self.get_academic_session()
	# 	user = self.request.user
	# 	form = StudentProfileModelForm()
	# 	institution = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution).first()
	# 	print("Institution1:", institution)
	# 	session = self.request.GET.get('academic_session')
	# 	# session = form['academic_session'].value()
	# 	print("Form Session:", session)
	# 	academic_session = AcademicSession.objects.get(id=session)
	# 	print("Academic Session1:", academic_session)
	# 	quota = AdmissionQuota.objects.get_or_none(institution = institution, academic_session = academic_session)
	# 	print("A Quota:", quota.admission_quota)
	# 	if quota.status == 0:
	# 		messages.error(self.request, "You can no longer index students for selected academic session. Please select an active academic session to proceed ")
	# 		return redirect("institutions:batch_create_student_profiles")
	# 	else:
	# 		return super(StudentProfileCreateView, self).dispatch(*args, **kwargs)

	# def get_academic_session(self, *args, **kwarg):
	# 	user = self.request.user
	# 	form = StudentProfileModelForm()
	# 	institution = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution).first()
	# 	print("Institution1:", institution)
	# 	session = self.request.GET.get('academic_session')
	# 	# session = form['academic_session'].value()
	# 	print("Form Session:", session)
	# 	academic_session = AcademicSession.objects.get(id=session)
	# 	print("Academic Session1:", academic_session)
	# 	quota = AdmissionQuota.objects.get_or_none(institution = institution, academic_session = academic_session)
	# 	print("A Quota:", quota.admission_quota)
	# 	return quota
		# if quota.active == False:
		# 	messages.error(request, "You can no longer index students for selected academic session. Please select an active academic session to proceed ")
		# 	return redirect("institutions:create_student_profile")
		# else:
		# 	return quota

	def get_form(self, *args, **kwargs):
		form = super(StudentProfileCreateView, self).get_form(*args, **kwargs)
		academic_session = self.get_academic_session()
		form.fields["academic_session"].queryset = academic_session
		return form


	
			
	def post(self, request, *args, **kwargs):
		user = self.request.user
		institution = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution).first()
		print("Institution:", institution)
		session = request.POST.get('academic_session')
		academic_session = AcademicSession.objects.get(id=session)
		print("Academic Session:", academic_session)
		quota = AdmissionQuota.objects.get_or_none(institution = institution, academic_session = academic_session)
		print("Quota:", quota)
		if quota is None:
			admission_quota = 0;
		else:
			admission_quota = quota.admission_quota
		print("Admission Quota:", admission_quota)
		students_qs = institution.studentprofile_set.all()
		# print("Queryset object:", admission_quota )
	
				
		# quota = AdmissionQuota.objects.filter(institution = user.get_indexing_officer_profile.institution)
		# admission_quota = quota.first()
		# academic_session = admission_quota.academic_session
		

		students_list = students_qs.filter(academic_session = academic_session)
		paramFile = io.TextIOWrapper(request.FILES['students_list'].file)
		portfolio1 = csv.DictReader(paramFile)
		list_of_dict = list(portfolio1)
		email_check = list_of_dict[0]["email"] == None

		try:
			context = {}
			if len(list_of_dict) == 0:
				messages.error(request, "No Data in List. Please populate list and try again")
				print("Number in List:",  len(list_of_dict))
				return redirect("institutions:batch_create_student_profiles")
			elif email_check:
				messages.error(request, "No email in list. Please add email and try again")
				print("Number of emails in List:",  len(data[0]["email"]))
				return redirect("institutions:batch_create_student_profiles")

			elif admission_quota == 0:
				messages.error(request, "No Quota Assigned for Selected Academic Session")
				print("Number in List:",  len(list_of_dict))
				print("Number of students registered:", len(students_list))
				print("Admission Quota:", int(admission_quota))
				return redirect("institutions:batch_create_student_profiles")



			elif len(students_list) > admission_quota or len(list_of_dict) > admission_quota or len(list_of_dict) + int(len(students_list)) > admission_quota:
				messages.error(request, "Admission Quota exceeded!")
				print("Number in List:",  len(list_of_dict))
				print("Number of students registered:", len(students_list))
				print("Admission Quotas:", int(admission_quota))
				return redirect("institutions:batch_create_student_profiles")

			# elif len(list_of_dict) > admission_quota:
			# 	messages.error(request, "Admission Quota exceeded!")	
			# 	print("Number in List:",  len(list_of_dict))
			# 	print("Number of students registered:", len(students_list))
			# 	print("Admission Quota:", int(admission_quota))			
			# 	print("Admission Quota exceeded")
			# 	return redirect("institutions:create_student_profile")

			else:
    		
				for row in list_of_dict:
					data = row['email']
					students_list = User.objects.filter(email = data)
					# print("Students:", students_list)
					try:
						if students_list.exists():
							for student in students_list:
								messages.error(request, f'This User: {student} and possibly other students on this list exit already exist')
							return redirect("institutions:batch_create_student_profiles")
						else:
							student = User.objects.create(email=row['email'], last_name=row['last_name'], first_name=row['first_name'], middle_name=row['middle_name'], phone_no=row['phone_no'], matric_no=row['matric_no'], password = make_password('student@001'),)
							
					except Exception as e:
						messages.error(request, e)

				objs = [
		            StudentProfile(
		            	student = User.objects.get(email=row['email']),
		            	institution=institution,
		            	academic_session = academic_session,
		            )
		            for row in list_of_dict   	
		         ]
				for obj in objs:
					obj.slug = create_slug3(instance=obj)
				nmsg = StudentProfile.objects.bulk_create(objs)
				messages.success(request, "Bulk Create of Students successful!")
				returnmsg = {"status_code": 200}
				for obj in objs:
					user = obj.student
					reset_password(user, request)
				# return redirect(institution.first().get_student_profiles_list())
				return redirect("institutions:batch_create_student_profiles")			
		except Exception as e:
			print('Error While Importing Data: ', e)
			returnmsg = {"status_code": 500}
		return JsonResponse(returnmsg)
		




class StudentProfileUpdateView (LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = "institutions/update_student_profile.html"
    # success_message = "Student Profile Update Successful"

    success_message = "%(student)s  Student Profile Update Successful"
    def get_object(self, queryset=None):
    	slug = self.kwargs.get("slug")
    	user = User.objects.get(slug=slug)
    	return user

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            student=self.object.get_full_name,
        )

    def get_success_url(self):
        return reverse("institutions:student_profiles_list") 


    def post(self, request, *args, **kwargs):
    	email = request.POST['email']
    	slug = self.kwargs.get("slug")
    	obj = get_object_or_404(User, slug=slug)
    	# obj = StudentProfile.objects.get(student__email= form.cleaned_data["email"]).student.email
    	form = self.form_class(request.POST or None, instance = obj)
    	if form.is_valid():
        	student_profile = form.save(commit=False)
        	student_profile.set_password("student@001")
        	student_profile.save()
        	user = student_profile
        	student_profile = StudentProfile.objects.filter(student=user).first()
        	print("User:", user)
        	# reset_password(user, request)
        	reset_user_password(user, self.request)
        	messages.success(request, 'Student Profile Update Successful')
        	return redirect(student_profile.get_absolute_url())
    	else:
        	messages.error(request, 'The email you are trying to assign to this student is already in use')
        	user = get_object_or_404(User, id=pk)
        	student_profile = StudentProfile.objects.filter(student=user).first()
        	return redirect(student_profile.get_absolute_url())

        	# form = self.form_class(request.POST or None, instance = obj)
        	# return render(request, self.template_name)
        	# return redirect("institutions:student_profiles_list")


        
    	return super(StudentProfileUpdateView, self).form_valid(form)
    	# return reverse("institutions:student_profiles_list") 
    	



class StudentProfileUpdateView1 (LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = SignupForm
    template_name = "institutions/update_student_profile.html"
    # success_message = "Student Profile Update Successful"

    success_message = "%(student)s  Student Profile Update Successful"
    def get_object(self, queryset=None):
    	pk = self.kwargs.get("pk")
    	user = User.objects.get(id=pk)
    	return user

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            student=self.object.get_full_name,
        )



    def get_success_url(self):
        # obj = self.get_object()
        # return reverse("indexing_unit:indexing_officer_detail" object.pk)
        return reverse("institutions:student_profiles_list") 

    # def form_valid(self, form):
    #     student_profile = form.save()
        # student = StudentProfile.objects.get(student__email= form.cleaned_data["email"]).student.email
        # user = student_profile
        # print ("User:", student)
        # user = student.student.email
        # print ("User Email:", user)
        # reset_user_password(user, self.request)
        # return super(StudentProfileUpdateView, self).form_valid(form)
    

    # def post(self, request, *args, **kwargs):
    # 	user = User(
    #         email=request.POST.get('email'),
    #         last_name=request.POST.get('last_name'),
    #         first_name=request.POST.get('first_name'),
    #         middle_name=request.POST.get('middle_name'),
    #         phone_no=request.POST.get('phone_no'),
    #         password=request.POST.get('password1'),
    #         role=request.POST.get('role'),
    #         )
    # 	user.save()
    # 	reset_user_password(user, self.request)

    def post(self, request, *args, **kwargs):
    	email = request.POST['email']
    	obj = get_object_or_404(User, email=email)
    	# obj = StudentProfile.objects.get(student__email= form.cleaned_data["email"]).student.email
    	form = self.form_class(request.POST or None, instance = obj)
    	if form.is_valid():
        	student_profile = form.save()
        	user = student_profile
        	reset_user_password(user, self.request)
    	return super(StudentProfileUpdateView, self).form_valid(form)
    	


            
    
        #     current_site = get_current_site(request)
        #     subject = 'Activate Your RRBN Portal Account'
        #     from_email = settings.DEFAULT_FROM_EMAIL
        #     to_email = [form.cleaned_data.get('email')]
        #     message = render_to_string('accounts/activation_request.html', {
        #         'user': user,
        #         'domain': current_site.domain,
        #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #         'token': account_activation_token.make_token(user),
        #     })
        #     send_mail(subject, message, from_email, to_email, fail_silently=True)

        #     messages.success(
        #         request, ('Please Confirm your email to complete registration.'))

        #     return render(request, self.template_name1)

        # return render(request, self.template_name, {'form': form})
        # return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # obj = self.get_object()
        # return reverse("indexing_unit:indexing_officer_detail" object.pk)
        return reverse("institutions:student_profiles_list") 
        # return HttpResponseRedirect("/"+id)

    



class StudentProfileCreateView1(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, CreateView):
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
			
			if len(students_list) >= int(admission_quota.admission_quota):
				messages.error(request, "Admission Quota exceeded!")				
				print("Admission Quota exceeded")
				return redirect("institutions:create_student_profile")
    		
			for row in list_of_dict:
				data = row['email']
				students_list = User.objects.filter(email = data)
				# print("Students:", students_list)
				try:
					if students_list.exists():
						for student in students_list:
							messages.error(request, f'This User: {student} and possibly other students on this list exit already exist')
						return redirect("institutions:create_student_profile")
					else:
						student = User.objects.create(email=row['email'], last_name=row['last_name'], first_name=row['first_name'], middle_name=row['middle_name'], phone_no=row['phone_no'], matric_no=row['matric_no'], password = make_password('Rebelspy1%'),)
						
				except Exception as e:
					messages.error(request, e)

			objs = [
	            StudentProfile(
	            	student = User.objects.get(email=row['email']),
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
			for obj in objs:
				user = obj.student
				reset_password(user, request)
			# return redirect(institution.first().get_student_profiles_list())
			return redirect("institutions:create_student_profile")			
		except Exception as e:
			print('Error While Importing Data: ', e)
			returnmsg = {"status_code": 500}
		return JsonResponse(returnmsg)



class StudentProfileCreateView2(StaffRequiredMixin, SuccessMessageMixin, CreateView):
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


class StudentProfileDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
	template_name = "institutions/student_profile_details.html"

	def get_object(self):
		institutionprofile_slug = self.kwargs.get("islug")
		studentprofile_slug = self.kwargs.get("sslug")
		obj = get_object_or_404(StudentProfile, institution__slug = institutionprofile_slug, slug = studentprofile_slug)
		return obj

# @user_passes_test(staff_required)


@login_required
def student_profiles_list7(request):
	academic_sessions = AcademicSession.objects.all()
	context = {'academic_sessions': academic_sessions}
	return render(request, 'institutions/academic_session_students_list.html', context)

@login_required
def student_list(request):
	academic_session = request.GET.get('academic_session')
	user = request.user
	# qs = InstitutionProfile.objects.filter(name=user.get_indexing_officer_profile.institution)
	# print ("Institution:", qs)
	# students_list = qs.first().studentprofile_set.all()
	students_list = StudentProfile.objects.filter(institution=user.get_indexing_officer_profile.institution, academic_session = academic_session)
	# print ("studens list:", students_list)
	context = {
	    'students_list':students_list,
	    }
	return render(request, 'partials/students_list.html', context)

@login_required
def student_profiles_list(request):
    selected_session_id = request.GET.get('academic_session')
    user = request.user

    # Save selected session to user's session
    if selected_session_id:
        request.session['selected_academic_session_id'] = selected_session_id
    else:
        # Try to recover from session if not sent
        selected_session_id = request.session.get('selected_academic_session_id')

    academic_sessions = AcademicSession.objects.all()

    # Check if user has an institution profile
    try:
        institution = user.get_indexing_officer_profile.institution
    except AttributeError:
        # If not, redirect or show error
        return redirect('login')  # or some error page


    students_list = StudentProfile.objects.filter(
        academic_session=selected_session_id, 
        institution=institution 
    )
    # if selected_session_id:
    #     applications = applications.filter(academic_session_id=selected_session_id)

    context = {
        'academic_sessions': academic_sessions,
        'students_list': students_list,
        'selected_session_id': selected_session_id,
    }
    if request.htmx:
        return render(request, 'partials/students_profile_list.html', context)
    return render(request, 'institutions/students_profile_list.html', context)



class StudentProfilesListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
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

class IndexedStudentsListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
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

class StudentIndexingApplicationsListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
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


class StudentIndexingApplicationDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
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


class StudentIndexingApplicationDetails(LoginRequiredMixin, StaffRequiredMixin, DetailView):
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


@login_required
def verify_application(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(StudentIndexing, slug=slug)
     # payment_object = object.indexingpayment_set.first()
     object.verification_status = "approved"
     # payment_object.payment_status = 2
     object.save()
     # payment_object.save()
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

@login_required
def reject_application(request, slug):
  if request.method == 'POST':
     object = get_object_or_404(StudentIndexing, slug=slug)
     # payment_object = object.indexingpayment_set.first()
     object.rejection_reason = request.POST.get('rejection_reason')
     object.rejection_status = "rejected"
     # payment_object.payment_status = 1
     object.save()
     # payment_object.save()
     context = {}
     context['object'] = object
     messages.error(request, ('Indexing Application Rejected'))
     return HttpResponseRedirect(reverse("institutions:student_indexing_application_details", kwargs={'islug': object.institution.slug,
            'sslug': object.slug,}))


@login_required
def verify_payment(request, id):
  if request.method == 'POST':
     object = get_object_or_404(IndexingPayment, pk=id)
     object.payment_status = 2
     object.save()
     context = {}
     context['object'] = object
     messages.success(request, ('Indexing Application Payment Verified'))
     return render(request, 'institutions/submitted_payment_details.html',context)

@login_required
def reject_payment(request, id):
  if request.method == 'POST':
     object = get_object_or_404(IndexingPayment, pk=id)
     object.payment_status = 1
     object.save()
     context = {}
     context['object'] = object
     # messages.error(request, ('Indexing Application Rejected'))
     return render(request, 'institutions/payment_verification_failed.html',context)

@login_required
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
		return qs.filter(verification_status="approved") 


class IndexingRejectionsListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
	template_name = "institutions/student_indexing_rejections_list.html"
	def get_queryset(self):
		request = self.request
		user = request.user
		qs = StudentIndexing.objects.filter(institution=user.get_indexing_officer_profile.institution)
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query)
		return qs.filter(rejection_status="rejected") 


class IndexingVerificationsDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
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




class IndexingRejectionsDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
	queryset = StudentIndexing.objects.all()
	template_name = "institutions/student_indexing_rejections_details.html"

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


class GenerateInvoiceView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    template_name = "institutions/generate_invoice.html"
    def get_queryset(self):
    	request = self.request
    	qs = StudentIndexing.objects.all()
    	query = request.GET.get('q')
    	if query:
    		qs = qs.filter(name__icontains=query)
    	return qs.filter(indexing_status=2) 



class IndexingPaymentCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = IndexingPayment
    template_name = "institutions/student_indexing_fee_payment.html"
    form_class = IndexingPaymentForm



class IndexingPaymentsListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
	template_name = "institutions/students_indexing_payments_list.html"
	queryset = IndexingPayment.objects.all()
	# def get_queryset(self):
	# 	request = self.request
	# 	qs = IndexingPayment.objects.all()
	# 	query = request.GET.get('q')
	# 	if query:
	# 		qs = qs.filter(name__icontains=query)
	# 	return qs.filter(indexing_status=3) 

class SubmittedPaymentsListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
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


class VerifiedPaymentsListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
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


class InstitutionsPaymentsListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
	template_name = "institutions/institutions_payments_list.html"
	
	def get_queryset(self):
		user = self.request.user
		try:
			obj = InstitutionIndexing.objects.filter(institution = user.get_indexing_officer_profile.institution)
			print ("obj:", obj)
			if obj.exists():
				return obj
		except:
			raise Http404



class StudentIndexingPaymentDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
	queryset = IndexingPayment.objects.all()
	template_name = "institutions/submitted_payment_details.html"


class IndexingPaymentsDetails(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "institutions/students_indexing_payments_details.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(IndexingPaymentsDetails, self).get_context_data(*args, **kwargs)
        context['object'] = IndexingPayment.objects.all()
        context['obj'] = InstitutionProfile.objects.filter(indexing_status=1)
        return context

@login_required
def students_applications_list0(request):
	academic_sessions = AcademicSession.objects.all()
	context = {'academic_sessions': academic_sessions}
	print("User Role:", request.user.role)
	return render(request, 'institutions/academic_sessions.html', context)


@login_required
def students_applications_list1(request):
    academic_sessions = AcademicSession.objects.all()

    selected_session = None
    applications = []

    if request.GET.get('academic_session'):
        selected_session = AcademicSession.objects.get(pk=request.GET.get('academic_session'))
        applications = StudentIndexing.objects.filter(academic_session=selected_session)

    context = {
        'academic_sessions': academic_sessions,
        'applications': applications,
        'selected_session': selected_session,
    }
    if request.htmx:
        return render(request, 'partials/applications_list.html', context)
    return render(request, 'institutions/applications_list.html', context)


@login_required
def students_applications_list(request):
    selected_session_id = request.GET.get('academic_session')
    user = request.user

    # Save selected session to user's session
    if selected_session_id:
        request.session['selected_academic_session_id'] = selected_session_id
    else:
        # Try to recover from session if not sent
        selected_session_id = request.session.get('selected_academic_session_id')

    academic_sessions = AcademicSession.objects.all()

    # Check if user has an institution profile
    try:
        institution = user.get_indexing_officer_profile.institution
    except AttributeError:
        # If not, redirect or show error
        return redirect('login')  # or some error page


    applications = StudentIndexing.objects.filter(
    	academic_session=selected_session_id, 
    	institution=institution, 
    	verification_status="pending", 
    	rejection_status = "pending"
    )
    # if selected_session_id:
    #     applications = applications.filter(academic_session_id=selected_session_id)

    context = {
        'academic_sessions': academic_sessions,
        'applications': applications,
        'selected_session_id': selected_session_id,
    }
    if request.htmx:
        return render(request, 'partials/applications_list.html', context)
    return render(request, 'institutions/applications_list.html', context)

# @login_required
# def applications_list(request):
# 	academic_session = request.GET.get('academic_session')
# 	user = request.user
# 	applications = StudentIndexing.objects.filter(academic_session=academic_session, institution=user.get_indexing_officer_profile.institution, verification_status="pending", rejection_status = "pending")
# 	context = {'applications': applications}
# 	return render(request, 'partials/applications_list.html', context)



@login_required
def students_verifications_list0(request):
	academic_sessions = AcademicSession.objects.all()
	context = {'academic_sessions': academic_sessions}
	# print("User Role:", request.user.role)
	return render(request, 'institutions/academic_session_verifications.html', context)

@login_required
def verifications_list(request):
	academic_session = request.GET.get('academic_session')
	user = request.user
	verifications = StudentIndexing.objects.filter(academic_session=academic_session, institution=user.get_indexing_officer_profile.institution, verification_status="approved").union(StudentIndexing.objects.filter(academic_session=academic_session, institution=user.get_indexing_officer_profile.institution, verification_status="indexed"))
	context = {'verifications': verifications}
	return render(request, 'partials/verifications.html', context)


def students_verifications_list(request):
    selected_session_id = request.GET.get('academic_session')
    user = request.user

    # Save selected session to user's session
    if selected_session_id:
        request.session['selected_academic_session_id'] = selected_session_id
    else:
        # Try to recover from session if not sent
        selected_session_id = request.session.get('selected_academic_session_id')

    academic_sessions = AcademicSession.objects.all()

    # Check if user has an institution profile
    try:
        institution = user.get_indexing_officer_profile.institution
    except AttributeError:
        # If not, redirect or show error
        return redirect('login')  # or some error page


    verifications = StudentIndexing.objects.filter(
    	academic_session=selected_session_id, 
    	institution=institution, 
    	verification_status="approved").union(StudentIndexing.objects.filter(
    	academic_session=selected_session_id, 
    	institution=institution, 
    	verification_status="indexed")
    	)
    # if selected_session_id:
    #     verifications = verifications.filter(academic_session_id=selected_session_id)

    context = {
        'academic_sessions': academic_sessions,
        'verifications': verifications,
        'selected_session_id': selected_session_id,
    }
    if request.htmx:
        return render(request, 'partials/verifications_list.html', context)
    return render(request, 'institutions/verifications_list.html', context)


@login_required
def students_rejections_list(request):
	academic_sessions = AcademicSession.objects.all()
	context = {'academic_sessions': academic_sessions}
	# print("User Role:", request.user.role)
	return render(request, 'institutions/academic_session_rejections.html', context)

@login_required
def rejections_list(request):
	academic_session = request.GET.get('academic_session')
	user = request.user
	rejections = StudentIndexing.objects.filter(academic_session=academic_session, institution=user.get_indexing_officer_profile.institution, rejection_status="rejected")
	context = {'rejections': rejections}
	return render(request, 'partials/rejections.html', context)





@login_required
def institutions_payments_list7(request):
	academic_sessions = AcademicSession.objects.all()
	context = {'academic_sessions': academic_sessions}
	return render(request, 'institutions/academic_session_payments.html', context)

@login_required
def payments_list(request):
	academic_session = request.GET.get('academic_session')
	user = request.user
	students_indexing = InstitutionIndexing.objects.filter(academic_session=academic_session, institution = user.get_indexing_officer_profile.institution)
	context = {'students_indexing': students_indexing}
	return render(request, 'partials/students_indexing.html', context)


@login_required
def institutions_payments_list(request):
    selected_session_id = request.GET.get('academic_session')
    user = request.user

    # Save selected session to user's session
    if selected_session_id:
        request.session['selected_academic_session_id'] = selected_session_id
    else:
        # Try to recover from session if not sent
        selected_session_id = request.session.get('selected_academic_session_id')

    academic_sessions = AcademicSession.objects.all()

    # Check if user has an institution profile
    try:
        institution = user.get_indexing_officer_profile.institution
    except AttributeError:
        # If not, redirect or show error
        return redirect('login')  # or some error page


    submissions = InstitutionIndexing.objects.filter(
    	academic_session=selected_session_id, 
    	institution=institution 
    )
    # if selected_session_id:
    #     applications = applications.filter(academic_session_id=selected_session_id)

    context = {
        'academic_sessions': academic_sessions,
        'submissions': submissions,
        'selected_session_id': selected_session_id,
    }
    if request.htmx:
        return render(request, 'partials/submissions_list.html', context)
    return render(request, 'institutions/submissions_list.html', context)

@login_required
def indexed_students_list7(request):
	academic_sessions = AcademicSession.objects.all()
	context = {'academic_sessions': academic_sessions}
	return render(request, 'institutions/academic_session_indexing_list.html', context)

@login_required
def indexed_list(request):
	academic_session = request.GET.get('academic_session')
	user = request.user
	institutions = InstitutionProfile.objects.filter(name = user.get_indexing_officer_profile.institution)
	indexing_list = IssueIndexing.objects.filter(academic_session=academic_session, institution__in=institutions)
	context = {
	    'institutions':institutions,
	    'indexing_list':indexing_list,
	    }
	return render(request, 'partials/indexed_students_list.html', context)


@login_required
def indexed_students_list(request):
    selected_session_id = request.GET.get('academic_session')
    user = request.user

    # Save selected session to user's session
    if selected_session_id:
        request.session['selected_academic_session_id'] = selected_session_id
    else:
        # Try to recover from session if not sent
        selected_session_id = request.session.get('selected_academic_session_id')

    academic_sessions = AcademicSession.objects.all()

    # Check if user has an institution profile
    try:
        institution = user.get_indexing_officer_profile.institution
    except AttributeError:
        # If not, redirect or show error
        return redirect('login')  # or some error page


    indexing_list = IssueIndexing.objects.filter(
        academic_session=selected_session_id, 
        institution=institution 
    )
    # if selected_session_id:
    #     applications = applications.filter(academic_session_id=selected_session_id)

    context = {
        'academic_sessions': academic_sessions,
        'indexing_list': indexing_list,
        'selected_session_id': selected_session_id,
    }
    if request.htmx:
        return render(request, 'partials/indexed_students_sessions_list.html', context)
    return render(request, 'institutions/indexed_students_sessions_list.html', context)


@login_required
def pay_institutions_indexing_fee(request):
	academic_sessions = AcademicSession.objects.all()
	academic_session = request.GET.get('academic_session')
	form = InstitutionIndexingModelForm(request.POST or None, request = request)
	context = {
		'academic_sessions': academic_sessions, 
		'academic_session': academic_session, 
		'form':form
	}
	return render(request, 'institutions/pay_institutions_indexing_fee.html', context)
	# return render(request, 'institutions/batch_process_students_indexing_payment.html', context)

class InstitutionPaymentCreateView(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = InstitutionIndexing
    template_name = "partials/institutions_payment_partial.html"
    # template_name = "partials/students_list_partial.html"
    form_class = InstitutionIndexingModelForm
    # success_message = "%(institution)s Institution Indexing Payment Submission Successful"
    academic_sessions = AcademicSession.objects.all()

    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	context['academic_sessions'] = AcademicSession.objects.all()
    	context['academic_session'] = self.request.GET.get('academic_session')
    	context['is_htmx'] = True
    	return context

    def get_form_kwargs(self):
        kwargs = super(InstitutionPaymentCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def post(self, request, *args, **kwargs):
    	user = self.request.user
    	session=request.POST.get('academic_session')
    	student_indexing = request.POST.getlist('student_indexing')
    	print ("List of Students:", student_indexing)
    	# students = StudentIndexing.objects.all()
    	try:
    		institution = user.get_indexing_officer_profile.institution
    	except AttributeError:
	        # If not, redirect or show error
	        return redirect('login')

    	institution_indexing = InstitutionIndexing.objects.create(
            # students_payments=request.POST.get('students_payments'),
            academic_session = AcademicSession.objects.get(id=session),
            rrr_number=request.POST.get('rrr_number'),
            payment_amount=request.POST.get('payment_amount'),
            payment_method=request.POST.get('payment_method'),
            payment_receipt=request.FILES.get('payment_receipt'),
            institution = InstitutionProfile.objects.get(name=institution),
            )

    	students = StudentIndexing.objects.filter(id__in=student_indexing)


    	institution_indexing.student_indexing.add(*students)
    	if not student_indexing:
		    messages.error(request, "Please select at least one student.")
		    return redirect("institutions:pay_institutions_indexing_fee")

    	# print ("Student Payments:", *student_indexing)
    	institution = institution_indexing.institution.name
    	# print ("institution:", institution)
    	messages.success(request, f"{institution}s Institution Indexing Submission Successful") 
    	return redirect(institution_indexing.get_absolute_url())


# def students_list_partial(request):
#     session_id = request.GET.get('academic_session')
#     students = StudentIndexing.objects.filter(academic_session_id=session_id) if session_id else []
#     return render(request, 'partials/students_list_partial.html', {'students': students})   	


def students_list_partial(request):
    academic_session_id = request.GET.get('academic_session')
    user = request.user

    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Authentication required")

    if not academic_session_id:
        return HttpResponseBadRequest("Academic session not provided")

    students = StudentIndexing.objects.filter(
        academic_session_id=academic_session_id,
        institution=user.get_indexing_officer_profile.institution,
        verification_status="pending",
        rejection_status="pending"
    )

    return render(request, 'partials/students_list_partial.html', {'students': students})
    	
def add_film(request):
    name = request.POST.get('name')
    
    # add film
    film = Film.objects.create(name=name)
    
    # add the film to the user's list
    request.user.films.add(film)

    # return template fragment with all the user's films
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})

class InstitutionPaymentCreateView1(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = InstitutionIndexing
    template_name = "institutions/pay_institutions_indexing_fee.html"
    form_class = InstitutionIndexingModelForm
    success_message = "%(institution)s Institution Indexing Payment Submission Successful"
    academic_sessions = AcademicSession.objects.all()


    # def get(self, request, *args, **kwargs):
    # 	form = InstitutionPaymentModelForm
    # 	academic_sessions = AcademicSession.objects.all()
    # 	template_name = "institutions/pay_institutions_indexing_fee.html"
    # 	return render(request, template_name, {'form':form})

    def get_success_message(self, cleaned_data):
      return self.success_message % dict(
            cleaned_data,
            institution=self.object.institution.name,
        )

    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	context['academic_sessions'] = AcademicSession.objects.all()
    	context['is_htmx'] = True
    	return context



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




class InstitutionPaymentsCreateView(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = InstitutionIndexing
    template_name = "institutions/institutions_indexing_payment.html"
    form_class = InstitutionIndexingModelForm
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
        


class InstitutionsIndexingPaymentDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
	queryset = InstitutionIndexing.objects.all()
	template_name = "institutions/institutions_payment_details.html"



class StudentIndexingNumberDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
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







