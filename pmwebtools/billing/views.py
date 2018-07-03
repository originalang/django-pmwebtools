from django.views import generic
from .models import historic_data
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from io import BytesIO, StringIO
import pandas as pd
import os
from django.contrib.auth.decorators  import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='pam:login')
def bill(request, department, billing_code, account_number_col_name, price_column_name):
	if request.method == "POST":
		file = request.FILES['uploaded_file']
		month_historic = historic_data()

		data = pd.read_excel(file, sheet_name=0)
		data = data[data[account_number_col_name] != 'Cash Only']

		col1 = pd.Series(['JL' for i in range(len(data))])
		col2 = pd.Series([billing_code for i in range(len(data))])
		col3 = pd.Series([(x + 1) for x in range(len(data))])

		account_number = data[account_number_col_name].str[:20]
		subsidiary = []
		for num in data[account_number_col_name]:
		    if len(num) > 20:
		        subsidiary.append(str(num[20:]))
		    else:
		        subsidiary.append('')

		sub_number = pd.Series(subsidiary)
		data = data.assign(col1=col1.values, col2=col2.values, col3=col3.values, account_number=account_number.values, subsidiary=sub_number.values)
		clean_data = data[['col1', 'col2', 'col3', price_column_name, 'Job Name', 'account_number', 'subsidiary']]

		file_title = request.POST.get('month') + ' ' + request.POST.get('year') + ' ' + department + ' for Accounting'

		excel_file = BytesIO()

		writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
		clean_data.to_excel(writer, 'Sheet1', header=False, index=False)
		writer.save()
		writer.close()
		excel_file.seek(0)

		total = '${:.2f}'.format(clean_data[price_column_name].sum())
		num_rows = str(len(clean_data))

		month_historic.department = department
		month_historic.month = request.POST.get('month')
		month_historic.year = request.POST.get('year')
		month_historic.amount = total
		month_historic.rows = int(num_rows.replace('Total Rows: ', ''))
		month_historic.file_name = file_title
		month_historic.excel_file = SimpleUploadedFile(file_title + '.xlsx', excel_file.read())
		month_historic.save()

		historic_id = month_historic.pk

		return render(request, 'billing/billing page.html', {'total':total, 'num_rows':num_rows, 'historic_id':historic_id})
	else:
		if department == 'Printing':
			return render(request, 'billing/upload_print_file.html')
		elif department == 'Mailing':
			return render(request, 'billing/upload_mail_file.html')


def bill_print(request):
	return bill(request, 'Printing', '7', 'Account Code', 'Order Price')


def bill_mail(request):
	return bill(request, 'Mailing', '6', 'Account Number', 'Total Plus Postage')

def download_excel_file(request, pk):
	historic_record = historic_data.objects.get(pk=pk)
	file_path = os.path.join(settings.MEDIA_ROOT, historic_record.excel_file.path)
	with open(file_path, 'rb') as f:
		response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(historic_record.file_name)
		return response


def download_txt_file(request, pk):
	historic_record = historic_data.objects.get(pk=pk)
	file_path = os.path.join(settings.MEDIA_ROOT, historic_record.excel_file.path)

	data = pd.read_excel(file_path, sheet_name=0, header=None)
	data[6] = data[6].astype(str).str.replace('nan', '').str.replace('\.0', '')

	tab_file = StringIO()
	data.to_csv(tab_file, sep='\t', header=False, index=False, line_terminator='\r\n')
	tab_file.seek(0)

	response = HttpResponse(tab_file.getvalue(), content_type='text/plain')
	tab_file.close()
	response['Content-Disposition'] = 'attachment; filename={}.txt'.format(historic_record.file_name)
	return response

class historic_billing_list(LoginRequiredMixin, generic.ListView):
	login_url = 'pam:login'
	redirect_field_name = None
	template_name = 'billing/historic_list.html'

	def get_queryset(self):
		return historic_data.objects.all()
