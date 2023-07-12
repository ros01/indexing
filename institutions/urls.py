from django.urls import path
from . import views
from .views import (
    DashboardView,
    StudentProfileCreateView,
    StudentProfileDetailView,
    # InstitutionCreateView,
    # InstitutionDetailView,
    StudentProfilesListView,
    StudentIndexingApplicationsListView,
    StudentIndexingApplicationDetailView,
    StudentIndexingApplicationDetails,
    IndexingVerificationsListView,
    IndexingVerificationsDetailView,
    IndexingPaymentsListView,
    GenerateInvoiceView,
    IndexingPaymentCreateView,
    IndexingPaymentsDetails,
    CreateAcademicSession,
    InstitutionPaymentCreateView,
    SubmittedPaymentsListView,
    VerifiedPaymentsListView,
    StudentIndexingPaymentDetailView,
    InstitutionsIndexingPaymentDetailView,
    InstitutionsPaymentsListView,
    AdmissionQuotaListView,
    AdmissionQuotaDetailView,

           
)


app_name = 'institutions'

urlpatterns = [
	path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('student_profiles_list/', StudentProfilesListView.as_view(), name='student_profiles_list'),
    path('create_student_profile',  StudentProfileCreateView.as_view(), name='create_student_profile'),
    path('downloadfile', views.downloadfile, name='downloadfile'),
    path('create_academic_session/', CreateAcademicSession.as_view(), name='create_academic_session'),
    path('student_profile_details/<slug:islug>/<slug:sslug>',  StudentProfileDetailView.as_view(), name='student_profile_details'),
    path('admission_quota_list',  AdmissionQuotaListView.as_view(), name='admission_quota_list'),
    path('<slug:slug>/admission_quota_detail',  AdmissionQuotaDetailView.as_view(), name='admission_quota_detail'),
    #path('student_profile_details/<slug:slug>',  StudentProfileDetailView.as_view(), name='student_profile_details'),
    path('student_indexing_applications_list', StudentIndexingApplicationsListView.as_view(), name='student_indexing_applications_list'),
    path('student_indexing_application_details/<slug:islug>/<slug:sslug>',  StudentIndexingApplicationDetailView.as_view(), name='student_indexing_application_details'),
    path('student_indexing_details/<slug:islug>/<slug:sslug>',  StudentIndexingApplicationDetails.as_view(), name='student_indexing_details'),
    path('student_indexing_verification_details/<slug:islug>/<slug:sslug>',  IndexingVerificationsDetailView.as_view(), name='student_indexing_verification_details'),
    path('<slug:slug>/verify_application/', views.verify_application, name='verify_application'),
    path('<slug:slug>/reject_application/', views.reject_application, name='reject_application'),
    path('<int:id>/verify_payment/', views.verify_payment, name='verify_payment'),
    path('<int:id>/reject_payment/', views.reject_payment, name='reject_payment'),
    path('institutions_indexing_payment',  InstitutionPaymentCreateView.as_view(), name='institutions_indexing_payment'),
    path('student_indexing_verifications_list', IndexingVerificationsListView.as_view(), name='student_indexing_verifications_list'),
    path('generate_payment_invoice', GenerateInvoiceView.as_view(), name='generate_payment_invoice'),
    path('student_indexing_payments_list', IndexingPaymentsListView.as_view(), name='student_indexing_payments_list'),
    path('make_indexing_payment',  IndexingPaymentCreateView.as_view(), name='make_indexing_payment'),
    path('view_indexing_payment_details',  IndexingPaymentsDetails.as_view(), name='view_indexing_payment_details'),
    path('submitted_payments_list', SubmittedPaymentsListView.as_view(), name='submitted_payments_list'),
    path('student_indexing_payment_details/<slug:slug>',  StudentIndexingPaymentDetailView.as_view(), name='student_indexing_payment_details'),
    path('verified_payments_list', VerifiedPaymentsListView.as_view(), name='verified_payments_list'),
    path('institutions_payments_list', InstitutionsPaymentsListView.as_view(), name='institutions_payments_list'),
    path('institutions_indexing_payment_details/<slug:slug>',  InstitutionsIndexingPaymentDetailView.as_view(), name='institutions_indexing_payment_details'),
    ]





    