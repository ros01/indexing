from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView
)
from django.views import View
from django.contrib.auth import get_user_model, update_session_auth_hash, authenticate, login as auth_login
from django.contrib import messages, auth
from .forms import SignupForm
from .models import *

AUTH_USER_MODEL = 'accounts.User'



class SigninTemplateView(TemplateView):
    template_name = "accounts/signin.html"

def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    user = auth.authenticate(email=email, password=password)
    if user is not None:
        auth_login(request, user)
        if user.role == 'Indexing Officer':
            return redirect('institutions:dashboard')
        if user.role == 'Indexing Unit':
            return redirect('indexing_unit:dashboard')
        if user.role == 'Student':
            return redirect('students:dashboard')
        if user.role == 'Registration':
            return redirect('registration:dashboard')
        else:
            messages.error(request, 'Please enter the correct email and password for your account. Note that both fields may be case-sensitive.')
            return redirect('accounts:signin')
    else:
        messages.error(request, 'Please enter the correct email and password for your account. Note that both fields may be case-sensitive.')
        return redirect('accounts:signin')




def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')



# class IndexingOfficerDetailView(DetailView):
#     queryset = IndexingOfficerProfile.objects.all()
#     template_name = "indexing_unit/indexing_officer_details.html"