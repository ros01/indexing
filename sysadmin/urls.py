from django.urls import path
from . import views
from .views import (
    SysAdminDashboard,
    

   
)


app_name = 'sysadmin'

urlpatterns = [
	path('dashboard/', SysAdminDashboard.as_view(), name='dashboard'),
    
	
    
    ]