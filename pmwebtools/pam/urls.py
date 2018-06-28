from django.urls import path, re_path
from . import views

app_name = 'pam'

urlpatterns = [
	path('', views.pam_home, name='pam-home'),
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
]
