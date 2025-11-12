from django.urls import path
from django.urls import re_path
from django.views.i18n import JavaScriptCatalog
from . import views
from .views import (
    DashboardView,
    InstitutionCreateView,
    InstitutionUpdateView,
    AcademicSessionCreateView,
    AcademicSessionDetailView,
    AcademicSessionUpdateView,
    IndexingOfficerCreateView,
    IndexingOfficerDetailView,
    IndexingOfficerDeleteView,
    IndexingOfficerUpdateView,
    IndexingOfficerListView,
    InstitutionDetailView,
    InstitutionDeleteView,
    InstitutionListView,
    InstitutionSearchView,
    AdmissionQuotaCreateView,
    AdmissionQuotaDetailView,
    AdmissionQuotaUpdateView,
    AdmissionQuotaListView,
    AcademicSessionListView,
    IndexingApplicationsListView,
    IndexingVerificationsDetailView,
    IndexNumberIssuanceList,
    IssueIndexNumberDetails,
    IssueIndexingNumber,
    IssuedIndexingApplications,
    IssuedIndexingApplicationsDetails,
    InstitutionAutocomplete,
    InstitutionsPaymentsListView,
    InstitutionsVerifiedPaymentsList,
    InstitutionsIndexingPaymentDetailView,
    VerifiedPaymentsListView,
    InstitutionsIndexingPreIssueDetailView,
    StudentIndexingApplicationDetailView,
    StudentIndexingNumberDetailView,
    
    InstitutionsIndexedStudentsList,
    InstitutionsIndexedStudentsListView,
    
    StudentsIndexingApplicationDetails,

       
)




app_name = 'indexing_unit'

# urls.py
from .views import IndexingOfficerDeleteView

app_name = 'indexing_unit'


urlpatterns = [
	path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('institutions_list', InstitutionListView.as_view(), name='institutions_list'),
    path('institutions_search_results', InstitutionSearchView.as_view(), name='institutions_search_results'),
    path('indexing_officers_list', IndexingOfficerListView.as_view(), name='indexing_officers_list'),
    # path('institutions_list', views.institutions_list, name='institutions_list'),
    path('universities_list', views.universities_list, name='universities_list'),
    # path('university_list', views.university_list, name='university_list'),
    path('academic_session_list',  AcademicSessionListView.as_view(), name='academic_session_list'),
    path('create_academic_session',  AcademicSessionCreateView.as_view(), name='create_academic_session'),
    path('<slug:slug>/update_academic_session',  AcademicSessionUpdateView.as_view(), name='update_academic_session'),
    path('<slug:slug>/activate_academic_session/', views.activate_academic_session, name='activate_academic_session'),
    path('<slug:slug>/deactivate_academic_session/', views.deactivate_academic_session, name='deactivate_academic_session'),
    path('assign_admission_quota',  AdmissionQuotaCreateView.as_view(), name='assign_admission_quota'),
    path('<slug:slug>/update_admission_quota/', AdmissionQuotaUpdateView.as_view(), name='update_admission_quota'),
    path('<slug:slug>/admission_quota_detail',  AdmissionQuotaDetailView.as_view(), name='admission_quota_detail'),
    path('admission_quota_list',  AdmissionQuotaListView.as_view(), name='admission_quota_list'),
    path('<slug:slug>/activate_institution_quota/', views.activate_institution_quota, name='activate_institution_quota'),
    path('<slug:slug>/deactivate_institution_quota/', views.deactivate_institution_quota, name='deactivate_institution_quota'),
    path('create_institution',  InstitutionCreateView.as_view(), name='create_institution'),
    path('<slug:slug>/update_institution',  InstitutionUpdateView.as_view(), name='update_institution'),
    path('create_indexing_officer',  IndexingOfficerCreateView.as_view(), name='create_indexing_officer'),
    path('<slug:slug>/institution_detail',  InstitutionDetailView.as_view(), name='institution_detail'),
    path('<slug:slug>/delete_institution/', InstitutionDeleteView.as_view(), name='delete_institution'),
    path('<slug:slug>/academic_session_detail',  AcademicSessionDetailView.as_view(), name='academic_session_detail'),
    path('<slug:slug>/indexing_officer_detail',  IndexingOfficerDetailView.as_view(), name='indexing_officer_detail'),
    path('<slug:slug>/delete_indexing_officer', IndexingOfficerDeleteView.as_view(), name='delete_indexing_officer'),
    path('<int:pk>/indexing_officer_update',  IndexingOfficerUpdateView.as_view(), name='indexing_officer_update'),
    path('<slug:slug>/activate_user/', views.activate_user, name='activate_user'),
    path('<slug:slug>/deactivate_user/', views.deactivate_user, name='deactivate_user'),
    path('institutions_payments_list', InstitutionsPaymentsListView.as_view(), name='institutions_payments_list'),
    path('institutions_verified_payments_list', InstitutionsVerifiedPaymentsList.as_view(), name='institutions_verified_payments_list'),
    path('students_indexing_applications', IndexingApplicationsListView.as_view(), name='students_indexing_applications'),
    path('students_index_number_list', IndexNumberIssuanceList.as_view(), name='students_index_number_list'),
    path('<slug:slug>/issue_index_number_details',  IssueIndexNumberDetails.as_view(), name='issue_index_number_details'),
    path('<slug:slug>/students_indexing_verification_details',  IndexingVerificationsDetailView.as_view(), name='students_indexing_verification_details'),
    path('<slug:slug>/issue_indexing_number',  IssueIndexingNumber.as_view(), name='issue_indexing_number'),
    # path('<int:id>/verify/', views.verify, name='verify'),
    # path('<int:id>/reject/', views.reject, name='reject'),
    path('issued_indexing_applications', IssuedIndexingApplications.as_view(), name='issued_indexing_applications'),
    path('<slug:slug>/issued_indexing_application_details',  IssuedIndexingApplicationsDetails.as_view(), name='issued_indexing_application_details'),
    path('institution_autocomplete', InstitutionAutocomplete.as_view(), name='institution_autocomplete'),
    path('institutions_indexing_payment_details/<slug:slug>',  InstitutionsIndexingPaymentDetailView.as_view(), name='institutions_indexing_payment_details'),
    path('institutions_indexing_pre_issue_details/<slug:slug>',  InstitutionsIndexingPreIssueDetailView.as_view(), name='institutions_indexing_pre_issue_details'),
    path('<slug:slug>/verify_payment/', views.verify_payment, name='verify_payment'),
    path('<slug:slug>/reject_payment/', views.reject_payment, name='reject_payment'),
    path('verified_payments_list', VerifiedPaymentsListView.as_view(), name='verified_payments_list'),

    path('students_indexing_details/<slug:islug>/<slug:sslug>',  StudentsIndexingApplicationDetails.as_view(), name='students_indexing_details'),
    path('student_indexing_details/<slug:islug>/<slug:sslug>',  StudentIndexingApplicationDetailView.as_view(), name='student_indexing_details'),
    path('<slug:slug>/approve_application/', views.approve_application, name='approve_application'),
    path('<slug:slug>/reject_application/', views.reject_application, name='reject_application'),
    path('student_indexing_number_details/<slug:slug>',  StudentIndexingNumberDetailView.as_view(), name='student_indexing_number_details'),
   
    path('indexed_students_list', InstitutionsIndexedStudentsList.as_view(), name='indexed_students_list'),
    path('institutions_indexed_students_list', InstitutionsIndexedStudentsListView.as_view(), name='institutions_indexed_students_list'),
    




    # re_path(r'^institution_autocomplete/$', InstitutionAutocomplete.as_view(), name='institution_autocomplete'),


    
    


    
    ]