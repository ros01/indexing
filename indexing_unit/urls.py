from django.urls import path
from django.urls import re_path
from django.views.i18n import JavaScriptCatalog
from . import views
from .views import (
    DashboardView,
    InstitutionCreateView,
    IndexingOfficerCreateView,
    IndexingOfficerDetailView,
    IndexingOfficerListView,
    InstitutionDetailView,
    InstitutionListView,
    AdmissionQuotaCreateView,
    AdmissionQuotaDetailView,
    AdmissionQuotaListView,
    IndexingApplicationsListView,
    IndexingVerificationsDetailView,
    IndexNumberIssuanceList,
    IssueIndexNumberDetails,
    IssueIndexingNumber,
    IssuedIndexingApplications,
    IssuedIndexingApplicationsDetails,
    InstitutionAutocomplete,
    InstitutionsPaymentsListView,
    InstitutionsIndexingPaymentDetailView,
    VerifiedPaymentsListView,
    InstitutionsIndexingPreIssueDetailView,
    StudentIndexingApplicationDetailView,
    StudentIndexingNumberDetailView,
    InstitutionsIndexingListView,
    InstitutionsIndexingStudentsListView,
    StudentsIndexingApplicationDetails,

       
)




app_name = 'indexing_unit'

urlpatterns = [
	path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('institutions_list', InstitutionListView.as_view(), name='institutions_list'),
    path('create_institution',  InstitutionCreateView.as_view(), name='create_institution'),
    path('create_indexing_officer',  IndexingOfficerCreateView.as_view(), name='create_indexing_officer'),
    path('indexing_officers_list', IndexingOfficerListView.as_view(), name='indexing_officers_list'),
    path('<slug:slug>/institution_detail',  InstitutionDetailView.as_view(), name='institution_detail'),
    path('<slug:slug>/indexing_officer_detail',  IndexingOfficerDetailView.as_view(), name='indexing_officer_detail'),
    path('assign_admission_quota',  AdmissionQuotaCreateView.as_view(), name='assign_admission_quota'),
    path('<slug:slug>/admission_quota_detail',  AdmissionQuotaDetailView.as_view(), name='admission_quota_detail'),
    path('admission_quota_list',  AdmissionQuotaListView.as_view(), name='admission_quota_list'),
    path('institutions_payments_list', InstitutionsPaymentsListView.as_view(), name='institutions_payments_list'),
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
    path('<int:id>/verify_payment/', views.verify_payment, name='verify_payment'),
    path('<int:id>/reject_payment/', views.reject_payment, name='reject_payment'),
    path('verified_payments_list', VerifiedPaymentsListView.as_view(), name='verified_payments_list'),

    path('students_indexing_details/<slug:islug>/<slug:sslug>',  StudentsIndexingApplicationDetails.as_view(), name='students_indexing_details'),
    path('student_indexing_details/<slug:islug>/<slug:sslug>',  StudentIndexingApplicationDetailView.as_view(), name='student_indexing_details'),
    path('<int:id>/verify/', views.verify, name='verify'),
    path('<int:id>/reject/', views.reject, name='reject'),
    path('student_indexing_number_details/<slug:slug>',  StudentIndexingNumberDetailView.as_view(), name='student_indexing_number_details'),
    path('institutions_indexing_list', InstitutionsIndexingListView.as_view(), name='institutions_indexing_list'),
    path('institutions_indexing_students_list', InstitutionsIndexingStudentsListView.as_view(), name='institutions_indexing_students_list'),
    




    # re_path(r'^institution_autocomplete/$', InstitutionAutocomplete.as_view(), name='institution_autocomplete'),


    
    


    
    ]