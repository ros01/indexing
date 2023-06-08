from . import views
from django.urls import path
from .views import (
    SigninTemplateView, 
    # IndexingOfficerDetailView,
    
)



app_name = 'accounts'


urlpatterns = [  
    #path('create_portal_account/', SignUpView.as_view(), name='create_portal_account'),
    path('signin', SigninTemplateView.as_view(), name='signin'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    # path('<slug:slug>/indexing_officer_detail',  IndexingOfficerDetailView.as_view(), name='indexing_officer_detail'),
   
]

