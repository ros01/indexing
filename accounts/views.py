from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView, 
     RedirectView,
     FormView,
)
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.views import View
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model, update_session_auth_hash, authenticate, login as auth_login
from django.contrib import messages, auth
from django.utils.encoding import force_str
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .forms import SignupForm
from .models import *
from django.urls import reverse_lazy
User = get_user_model()

AUTH_USER_MODEL = 'accounts.User'



class SigninTemplateView(TemplateView):
    template_name = "accounts/signin.html"



class ActivateView(RedirectView):

    url = reverse_lazy('students:dashboard')


    # Custom get method
    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            auth_login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request, 'accounts/activate_account_invalid.html')

class CheckEmailView(TemplateView):
    template_name = 'accounts/check_email.html'

class SuccessView(TemplateView):
    template_name = 'accounts/success.html'


class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password-reset-complete')
    form_valid_message = ("Your password was changed!")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password-reset-done')
    # success_url = reverse_lazy('accounts:password_reset_complete')
    #subject_template_name = 'accounts/emails/password-reset-subject.txt'
    email_template_name = 'accounts/password_reset_email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_valid_message = ("Your password was changed!")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'



class PasswordResetConfirmView2(FormView):
    template_name = "account/password_reset_comfirmation.html"
    success_url = '/accounts/password_reset_success'
    form_class = SetPasswordForm
    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['confirmation']
                user.password = hashlib.sha256(new_password.encode('utf8')).hexdigest()
                user.save()
                messages.success(request, 'Your password has been modified')
                return self.form_valid(form)
            else:
                print(form.errors)
                messages.error(request, form.errors)
                return self.form_invalid(form)
        else:
            messages.error(
                request, 'This link has expired.')
            return self.form_invalid(form)


def password_reset_success(request):
    return render(request,'accounts/password_reset_successful.html',{})



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