from django.db import models
from django.urls import reverse


class department(models.Model):
	department_name = models.CharField(max_length=100)
	contact_name = models.CharField(max_length=100)
	contact_email = models.CharField(max_length=100)
	contact_phone = models.CharField(max_length=14)

	def __str__(self):
		return self.department_name

	def get_absolute_url(self):
		return reverse('inventory:stock_detail', kwargs={'pk':self.pk})


class managed_stock(models.Model):
	department = models.ForeignKey(department, on_delete=models.PROTECT)
	stock_id = models.CharField(max_length=10)
	stock_name = models.CharField(max_length=50)
	threshold = models.IntegerField()
	current_inventory = models.IntegerField(default=0, blank=True)

	def get_absolute_url(self):
		return reverse('inventory:stock_detail', kwargs={'pk':self.department_id})
