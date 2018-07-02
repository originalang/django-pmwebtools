from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse

tag_choices = (
	('Webdesk', 'Webdesk'),
	('Printing', 'Printing'),
	('Mailing', 'Mailing'),
	('Management', 'Management'),
	('Administration', 'Administration'),
	('Students', 'Students'),
	)

class theme(models.Model):
	theme_name = models.CharField(max_length=60)
	tag = models.CharField(max_length=150, choices=tag_choices)
	theme_description = models.CharField(max_length=900)

	def __str__(self):
		return self.theme_name

	def get_absolute_url(self):
		return reverse('repository:topic_index', kwargs={'pk':self.id})

	def number_of_topics(self):
		return len(self.topic_set.all())


class topic(models.Model):
	topic_theme = models.ForeignKey(theme, on_delete=models.PROTECT)
	topic_title = models.CharField(max_length=255)
	topic_description = HTMLField()

	def get_absolute_url(self):
		return reverse('repository:topic_index', kwargs={'pk':self.topic_theme.id})

	def topic_description_preview(self):
		if(len(self.topic_description) < 100):
			return self.topic_description.replace('\n', ' ')
		else:
			return self.topic_description[:100].replace('\n', ' ') + '...'
