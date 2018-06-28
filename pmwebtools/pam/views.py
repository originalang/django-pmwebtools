from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='pam:login')
def pam_home(request):
	return render(request, 'home/homepage.html', {})


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
