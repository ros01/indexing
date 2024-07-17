from django.urls import path
from . import views
from .views import (
    DashboardView,
    InstitutionListView,
    InstitutionDetailView,
    IndexingOfficerListView,
    IndexingOfficerDetailView,
    AdmissionQuotaListView,
    AdmissionQuotaDetailView,
    # InstitutionsPaymentsListView,
    # InstitutionsVerifiedPaymentsList,
    IndexNumberIssuanceListView,
    IndexNumberIssuanceList,
    InstitutionsIndexingPreIssueDetailView,
    StudentIndexingVerifiedDetails,
    StudentsIndexingApplicationDetails,
    StudentsPostIndexingDetails,
    IssueIndexingNumber,
    InstitutionsIndexedStudentsList,
    InstitutionsIndexedStudentsListView,
    StudentIndexingNumberDetailView,
    StudentIndexingApplicationDetailView,
    InstitutionsIndexingPaymentDetailView,
    InstitutionsIndexingPaymentVerifiedDetailView,
           
)


app_name = 'registration'

urlpatterns = [
	path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('institutions_list', InstitutionListView.as_view(), name='institutions_list'),
    path('<slug:slug>/institution_detail',  InstitutionDetailView.as_view(), name='institution_detail'),
    path('indexing_officers_list', IndexingOfficerListView.as_view(), name='indexing_officers_list'),
    path('<slug:slug>/indexing_officer_detail',  IndexingOfficerDetailView.as_view(), name='indexing_officer_detail'),
    path('admission_quota_list',  AdmissionQuotaListView.as_view(), name='admission_quota_list'),
    path('<slug:slug>/admission_quota_detail',  AdmissionQuotaDetailView.as_view(), name='admission_quota_detail'),
    path('institutions_payments_list', views.institutions_payments_list, name='institutions_payments_list'),
    path('payments_list', views.payments_list, name='payments_list'),
    # path('institutions_payments_list', InstitutionsPaymentsListView.as_view(), name='institutions_payments_list'),
    path('institutions_verified_payments_list', views.institutions_verified_payments_list, name='institutions_verified_payments_list'),
    path('verified_payments_list', views.verified_payments_list, name='verified_payments_list'),
    # path('institutions_verified_payments_list', InstitutionsVerifiedPaymentsList.as_view(), name='institutions_verified_payments_list'),

    # path('students_index_number_list', views.students_index_number_list, name='students_index_number_list'),
    path('select_institution', views.select_institution, name='select_institution'),
    path('indexing_numbers_list', views.indexing_numbers_list, name='indexing_numbers_list'),
    path('institutions_indexing_number_list', IndexNumberIssuanceListView.as_view(), name='institutions_indexing_number_list'),
    path('students_index_number_list', IndexNumberIssuanceList.as_view(), name='students_index_number_list'),
    path('institutions_indexing_pre_issue_details/<slug:slug>',  InstitutionsIndexingPreIssueDetailView.as_view(), name='institutions_indexing_pre_issue_details'),
    path('<slug:slug>/issue_indexing_number',  IssueIndexingNumber.as_view(), name='issue_indexing_number'),
    
    path('indexed_students_list', InstitutionsIndexedStudentsList.as_view(), name='indexed_students_list'),
    path('institutions_indexed_students_list', InstitutionsIndexedStudentsListView.as_view(), name='institutions_indexed_students_list'),
    
    path('student_indexing_details/<slug:islug>/<slug:sslug>',  StudentIndexingApplicationDetailView.as_view(), name='student_indexing_details'),
    path('student_indexing_verified_details/<slug:islug>/<slug:sslug>',  StudentIndexingVerifiedDetails.as_view(), name='student_indexing_verified_details'),
    path('students_indexing_details/<slug:islug>/<slug:sslug>',  StudentsIndexingApplicationDetails.as_view(), name='students_indexing_details'),
    path('students_post_indexing_details/<slug:islug>/<slug:sslug>',  StudentsPostIndexingDetails.as_view(), name='students_post_indexing_details'),
    path('student_indexing_number_details/<slug:slug>',  StudentIndexingNumberDetailView.as_view(), name='student_indexing_number_details'),
    path('<slug:slug>/approve_application/', views.approve_application, name='approve_application'),
    path('<slug:slug>/reject_application/', views.reject_application, name='reject_application'),
    path('<slug:slug>/verify_payment/', views.verify_payment, name='verify_payment'),
    path('<slug:slug>/reject_payment/', views.reject_payment, name='reject_payment'),
    path('institutions_indexing_payment_details/<slug:slug>',  InstitutionsIndexingPaymentDetailView.as_view(), name='institutions_indexing_payment_details'),
    path('institutions_indexing_payment_verified_details/<slug:slug>',  InstitutionsIndexingPaymentVerifiedDetailView.as_view(), name='institutions_indexing_payment_verified_details'),

    ]





    