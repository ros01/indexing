from . import views
from django.urls import path
from .views import (
    SigninTemplateView, 
    ActivateView,
    CheckEmailView,
    SuccessView,
    # PasswordResetView,

    # IndexingOfficerDetailView,
    
)
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


app_name = 'accounts'


urlpatterns = [  
    #path('create_portal_account/', SignUpView.as_view(), name='create_portal_account'),
    path('signin', SigninTemplateView.as_view(), name='signin'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name="activate"),
    path('check-email/', CheckEmailView.as_view(), name="check_email"),
    path('success/', SuccessView.as_view(), name="success"),
    path('password-change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-done/', views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset_password/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset_password_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_success', views.password_reset_success, name="password_reset_success"),
    # path('reset_password', sendPasswordLink, name="reset_password"),
    # path('password-reset/', 
    #     PasswordResetView.as_view(
    #         template_name='accounts/password_reset.html',
    #         html_email_template_name='accounts/password_reset_email.html'
    #     ),
    #     name='password-reset'
    # ),
    # path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    # path('password_reset_confirm/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    # path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    # path('<slug:slug>/indexing_officer_detail',  IndexingOfficerDetailView.as_view(), name='indexing_officer_detail'),
   
]

