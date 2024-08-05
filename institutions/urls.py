from django.urls import path
from . import views
from .views import (
    DashboardView,
    StudentProfileCreateView,
    StudentProfileDetailView,
    StudentProfileUpdateView,
    # InstitutionCreateView,
    # InstitutionDetailView,
    # StudentProfilesListView,
    # StudentIndexingApplicationsListView,
    StudentIndexingApplicationDetailView,
    StudentIndexingApplicationDetails,
    # IndexingVerificationsListView,
    IndexingVerificationsDetailView,
    IndexingRejectionsDetailView,
    IndexingPaymentsListView,
    GenerateInvoiceView,
    IndexingPaymentCreateView,
    IndexingPaymentsDetails,
    # CreateAcademicSession,
    InstitutionPaymentCreateView,
    InstitutionPaymentsCreateView,
    SubmittedPaymentsListView,
    VerifiedPaymentsListView,
    StudentIndexingPaymentDetailView,
    InstitutionsIndexingPaymentDetailView,
    # InstitutionsPaymentsListView,
    AdmissionQuotaListView,
    AdmissionQuotaDetailView,
    InstitutionDetailView,
    # IndexedStudentsListView,
    StudentIndexingNumberDetailView,


           
)


app_name = 'institutions'

urlpatterns = [
	path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('<slug:slug>/institution_detail',  InstitutionDetailView.as_view(), name='institution_detail'),
    path('admission_quota_list',  AdmissionQuotaListView.as_view(), name='admission_quota_list'),
    path('student_indexing_applications_list', views.students_applications_list, name='student_indexing_applications_list'),
    path('applications_list', views.applications_list, name='applications_list'),
    path('student_indexing_verifications_list', views.students_verifications_list, name='student_indexing_verifications_list'),
    path('verifications_list', views.verifications_list, name='verifications_list'),
    path('student_indexing_rejections_list', views.students_rejections_list, name='student_indexing_rejections_list'),
    path('rejections_list', views.rejections_list, name='rejections_list'),
    path('institutions_payments_list', views.institutions_payments_list, name='institutions_payments_list'),
    path('payments_list', views.payments_list, name='payments_list'),

    path('indexed_students_list', views.indexed_students_list, name='indexed_students_list'),
    path('indexed_list', views.indexed_list, name='indexed_list'),

    path('student_profiles_list', views.student_profiles_list, name='student_profiles_list'),
    path('student_list', views.student_list, name='student_list'),


    # path('student_profiles_list/', StudentProfilesListView.as_view(), name='student_profiles_list'),
    # path('indexed_students_list', IndexedStudentsListView.as_view(), name='indexed_students_list'),
    # path('institutions_payments_list', InstitutionsPaymentsListView.as_view(), name='institutions_payments_list'),
    # path('student_indexing_verifications_list', IndexingVerificationsListView.as_view(), name='student_indexing_verifications_list'),

    path('<slug:slug>/admission_quota_detail',  AdmissionQuotaDetailView.as_view(), name='admission_quota_detail'),
    path('pay_institutions_indexing_fee',  views.pay_institutions_indexing_fee, name='pay_institutions_indexing_fee'),
    path('pay_session_indexing_fee',  InstitutionPaymentCreateView.as_view(), name='pay_session_indexing_fee'),

    path('batch_create_student_profiles',  views.batch_create_student_profiles, name='batch_create_student_profiles'),
    path('create_student_profile',  StudentProfileCreateView.as_view(), name='create_student_profile'),
    path('<int:pk>/student_profile_update',  StudentProfileUpdateView.as_view(), name='student_profile_update'),


    path('downloadfile', views.downloadfile, name='downloadfile'),
    # path('create_academic_session/', CreateAcademicSession.as_view(), name='create_academic_session'),
    path('student_profile_details/<slug:islug>/<slug:sslug>',  StudentProfileDetailView.as_view(), name='student_profile_details'),
    #path('student_profile_details/<slug:slug>',  StudentProfileDetailView.as_view(), name='student_profile_details'),
    

    # path('student_indexing_applications_list', StudentIndexingApplicationsListView.as_view(), name='student_indexing_applications_list'),
    
    path('student_indexing_application_details/<slug:islug>/<slug:sslug>',  StudentIndexingApplicationDetailView.as_view(), name='student_indexing_application_details'),
    path('student_indexing_details/<slug:islug>/<slug:sslug>',  StudentIndexingApplicationDetails.as_view(), name='student_indexing_details'),
    path('student_indexing_verification_details/<slug:islug>/<slug:sslug>',  IndexingVerificationsDetailView.as_view(), name='student_indexing_verification_details'),
    path('student_indexing_rejection_details/<slug:islug>/<slug:sslug>',  IndexingRejectionsDetailView.as_view(), name='student_indexing_rejection_details'),
    path('<slug:slug>/verify_application/', views.verify_application, name='verify_application'),
    path('<slug:slug>/reject_application/', views.reject_application, name='reject_application'),
    path('<int:id>/verify_payment/', views.verify_payment, name='verify_payment'),
    path('<int:id>/reject_payment/', views.reject_payment, name='reject_payment'),
    path('pay_institutions_indexing_fee',  views.pay_institutions_indexing_fee, name='pay_institutions_indexing_fee'),
    
    path('pay_session_indexing_fee',  InstitutionPaymentCreateView.as_view(), name='pay_session_indexing_fee'),
    path('pay_institution_indexing_fee',  InstitutionPaymentsCreateView.as_view(), name='pay_institution_indexing_fee'),
    
    path('generate_payment_invoice', GenerateInvoiceView.as_view(), name='generate_payment_invoice'),
    path('student_indexing_payments_list', IndexingPaymentsListView.as_view(), name='student_indexing_payments_list'),
    path('make_indexing_payment',  IndexingPaymentCreateView.as_view(), name='make_indexing_payment'),
    path('view_indexing_payment_details',  IndexingPaymentsDetails.as_view(), name='view_indexing_payment_details'),
    path('submitted_payments_list', SubmittedPaymentsListView.as_view(), name='submitted_payments_list'),
    path('student_indexing_payment_details/<slug:slug>',  StudentIndexingPaymentDetailView.as_view(), name='student_indexing_payment_details'),
    path('verified_payments_list', VerifiedPaymentsListView.as_view(), name='verified_payments_list'),
    path('institutions_indexing_payment_details/<slug:slug>',  InstitutionsIndexingPaymentDetailView.as_view(), name='institutions_indexing_payment_details'),
    path('student_indexing_number_details/<slug:slug>',  StudentIndexingNumberDetailView.as_view(), name='student_indexing_number_details'),
    ]





    