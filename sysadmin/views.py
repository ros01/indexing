from django.shortcuts import render
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
User = get_user_model()


class StaffRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'Sysadmin':
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request,
            *args, **kwargs)


# Create your views here.
class DashboardTemplateView(TemplateView):
    template_name = "sysadmin/sysadmin_dashboard.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        return context


class SysAdminDashboard(StaffRequiredMixin, ListView):
	template_name = "sysadmin/sysadmin_dashboard.html"
	def get_queryset(self):
		request = self.request
		# qs = User.objects.filter(role='Indexing Officer')
		qs = User.objects.exclude(role = "")
		query = request.GET.get('q')
		if query:
			qs = qs.filter(name__icontains=query).distinct()
		return qs  #.filter(title__icontains='vid')

	def get_context_data(self, *args, **kwargs):
		context = super(SysAdminDashboard, self).get_context_data(*args, **kwargs)
		context['sys'] = User.objects.filter(role="Sysadmin")
		context['ind'] = User.objects.filter(role="Indexing Unit")
		return context





