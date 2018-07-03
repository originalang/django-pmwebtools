from django.db import models


class historic_data(models.Model):
	department = models.CharField(max_length=15)
	month = models.CharField(max_length=20)
	year = models.CharField(max_length=4)
	amount = models.CharField(max_length=10)
	rows = models.IntegerField()
	file_name = models.CharField(max_length=50)
	excel_file = models.FileField()
	tab_delimited_file = models.FileField()
