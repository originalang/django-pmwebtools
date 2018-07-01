from django.urls import path, re_path
from . import views

app_name = 'inventory'

urlpatterns = [
	path('department/add', views.DepartmentCreate.as_view(), name='department-add'),
	re_path(r'department:(?P<pk>[0-9]+)/stock/add/$', views.ManagedStockCreate.as_view(), name='stock-add'),


	re_path(r'department/(?P<pk>[0-9]+)/$', views.DepartmentUpdate.as_view(), name='department-update'),
	re_path(r'stock/(?P<pk>[0-9]+)/$', views.ManagedStockUpdate.as_view(), name='stock-update'),


	re_path(r'department/(?P<pk>[0-9]+)/delete/$', views.DepartmentDelete.as_view(), name='department-delete'),
	re_path(r'stock/(?P<pk>[0-9]+)/delete/$', views.ManagedStockDelete.as_view(), name='stock-delete'),

	path('login/psp/', views.psp_login, name='psp-login'),
#	path('update_inv', views.get_current_inv, name='get-inv'),


	re_path(r'^(?P<pk>[0-9]+)/$', views.stock_detail.as_view(), name='stock_detail'),
	path('', views.IndexView.as_view(), name='index'),
]
