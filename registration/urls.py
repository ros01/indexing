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
    IndexNumberIssuanceList,
    InstitutionsIndexingPreIssueDetailView,
    StudentsIndexingApplicationDetails,
    IssueIndexingNumber,
    InstitutionsIndexedStudentsListView,
    StudentIndexingNumberDetailView,
    StudentIndexingApplicationDetailView,



    
    

           
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
    path('students_index_number_list', IndexNumberIssuanceList.as_view(), name='students_index_number_list'),
    path('institutions_indexing_pre_issue_details/<slug:slug>',  InstitutionsIndexingPreIssueDetailView.as_view(), name='institutions_indexing_pre_issue_details'),
    path('<slug:slug>/issue_indexing_number',  IssueIndexingNumber.as_view(), name='issue_indexing_number'),
    path('institutions_indexed_students_list', InstitutionsIndexedStudentsListView.as_view(), name='institutions_indexed_students_list'),
    path('student_indexing_details/<slug:islug>/<slug:sslug>',  StudentIndexingApplicationDetailView.as_view(), name='student_indexing_details'),
    path('students_indexing_details/<slug:islug>/<slug:sslug>',  StudentsIndexingApplicationDetails.as_view(), name='students_indexing_details'),
    path('student_indexing_number_details/<slug:slug>',  StudentIndexingNumberDetailView.as_view(), name='student_indexing_number_details'),

    ]





    