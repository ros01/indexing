from django.urls import path
from . import views
from .views import (
    DashboardView,
    # StudentProfileCreateView,
    # StudentProfileDetailView,
    IndexingApplicationCreateView,
    IndexingPaymentCreateView,
    UpdateProfile,
    # InstitutionDetailView,
    MyIndexingApplicationListView,
    MyStudentProfileListView,
    ApplicationList,
    MyStudentProfileDetailView,
    MyIndexingApplicationListView,
    MyIndexingApplicationDetailView,
    MyIndexingPaymentDetailView,
    MyIndexingPaymentListView,
    IndexingPaymentCreateListView,
    # MyApplicationStatus,
       
)


app_name = 'students'

urlpatterns = [
	path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('application_history/', views.status, name='application_history'),
    path('my_student_profile_list', MyStudentProfileListView.as_view(), name='my_student_profile_list'),
    path('application_list', ApplicationList.as_view(), name='application_list'),
    path('update_profile/<slug:slug>', UpdateProfile.as_view(), name='update_profile'),
    # path('my_indexing_application', MyIndexingApplicationListView.as_view(), name='my_indexing_application'),
    path('start_indexing_application',  IndexingApplicationCreateView.as_view(), name='start_indexing_application'),
    path('start_indexing_application_payment',  IndexingPaymentCreateListView.as_view(), name='start_indexing_application_payment'),
    path('indexing_application_payment',  IndexingPaymentCreateView.as_view(), name='indexing_application_payment'),
    path('my_student_profile_details/<slug:slug>',  MyStudentProfileDetailView.as_view(), name='my_student_profile_details'),
    path('my_indexing_application/', views.status, name='my_indexing_application'),
    # path('my_application_status', MyApplicationStatus.as_view(), name='my_application_status'),
    path('my_indexing_application_list', MyIndexingApplicationListView.as_view(), name='my_indexing_application_list'),
    path('my_indexing_application_details/<slug:slug>',  MyIndexingApplicationDetailView.as_view(), name='my_indexing_application_details'),
    path('my_indexing_payment_list', MyIndexingPaymentListView.as_view(), name='my_indexing_payment_list'),
    path('my_indexing_payment_details/<slug:slug>',  MyIndexingPaymentDetailView.as_view(), name='my_indexing_payment_details'),
    
    # path('assign_admission_quota',  AdmissionQuotaCreateView.as_view(), name='assign_admission_quota'),
    # path('<slug:slug>/admission_quota_detail',  AdmissionQuotaDetailView.as_view(), name='admission_quota_detail'),
    # path('admission_quota_list',  AdmissionQuotaListView.as_view(), name='admission_quota_list'),
    


    
    ]