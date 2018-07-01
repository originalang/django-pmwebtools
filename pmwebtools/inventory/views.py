from django.views import generic
from .models import managed_stock, department
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators  import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, generic.ListView):
	login_url = 'pam:login'
	template_name = 'inventory/stock_home.html'

	def get_queryset(self):
		return department.objects.all()


class stock_detail(LoginRequiredMixin, generic.DetailView):
	login_url = 'pam:login'
	model = department
	template_name = 'inventory/stock_detail.html'


class DepartmentCreate(LoginRequiredMixin, CreateView):
	login_url = 'pam:login'
	model = department
	fields = '__all__'


class ManagedStockCreate(LoginRequiredMixin, CreateView):
	login_url = 'pam:login'
	model = managed_stock
	fields = ['stock_id', 'stock_name', 'threshold', 'inventory_url']

	def form_valid(self, form):
		form.instance.department_id = self.kwargs['pk']
		return super(ManagedStockCreate, self).form_valid(form)


class DepartmentUpdate(LoginRequiredMixin, UpdateView):
	login_url = 'pam:login'
	model = department
	fields = '__all__'


class ManagedStockUpdate(LoginRequiredMixin, UpdateView):
	login_url = 'pam:login'
	model = managed_stock
	fields = ['stock_id', 'stock_name', 'threshold', 'inventory_url']


class DepartmentDelete(LoginRequiredMixin, DeleteView):
	login_url = 'pam:login'
	model = department
	success_url = reverse_lazy('inventory:index')

class ManagedStockDelete(LoginRequiredMixin, DeleteView):
	login_url = 'pam:login'
	model = managed_stock

	def get_success_url(self):
		dep_id = managed_stock.objects.get(pk=self.kwargs['pk']).department.id
		return reverse_lazy('inventory:stock_detail', kwargs={'pk':dep_id})

@login_required(login_url='pam:login')
def psp_login(request):
	return render(request, 'inventory/psp_login.html')
