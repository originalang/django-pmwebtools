from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='pam:login')
def pam_home(request):
	return render(request, 'home/homepage.html', {})


class RegistrationFormView(View):
	form_class = RegistrationForm
	template_name = 'home/registration.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('pam:pam-home')

		return render(request, self.template_name, {'form':form})


def login_view(request):
	if request.method == 'GET':
		return render(request, 'home/login.html')

	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('pam:pam-home')

		return render(request, 'home/login.html')


def logout_view(request):
	logout(request)
	return redirect('pam:login')
