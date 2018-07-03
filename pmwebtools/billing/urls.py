from django.contrib import admin
from django.urls import include, path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'billing'

urlpatterns = [
	path('printing/bill/', views.bill_print, name='bill_print'),
	path('mailing/bill/', views.bill_mail, name='bill_mail'),
	path('historic_data', views.historic_billing_list.as_view(), name='historic_billing_list'),
	re_path(r'historic_data/excel/(?P<pk>[0-9]+)/$', views.download_excel_file, name='download_excel_file'),
	re_path(r'historic_data/txt/(?P<pk>[0-9]+)/$', views.download_txt_file, name='download_txt_file'),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
