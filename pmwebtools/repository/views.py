from django.shortcuts import render
from django.http import HttpResponse
from .models import theme, topic
from django.db.models import Q
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators  import login_required

@login_required(login_url='pam:login')
def theme_index(request):
	query = request.GET.get('search_themes')
	theme_queryset = theme.objects.all()
	if query:
		theme_queryset = theme_queryset.filter(theme_name__icontains=query)
		return render(request, 'repository/theme_index.html', {'theme_queryset':theme_queryset, 'query':query})
	else:
		return render(request, 'repository/theme_index.html', {'theme_queryset':theme_queryset, 'query':''})


def topic_index(request, pk):
	query = request.GET.get('search_topics')
	theme_query = theme.objects.get(pk=pk)
	topic_queryset = theme_query.topic_set.all()
	if query:
		topic_queryset = topic_queryset.filter(
											Q(topic_title__icontains=query) |
											Q(topic_description__icontains=query)
										)
		return render(request, 'repository/topic_index.html', {'theme_query':theme_query, 'topic_queryset':topic_queryset, 'query':query})
	else:
		return render(request, 'repository/topic_index.html', {'theme_query':theme_query, 'topic_queryset':topic_queryset, 'query':''})


class topic_detail(generic.DetailView):
	model = topic
	template_name = 'repository/topic_detail.html'


class themeCreate(CreateView):
	model = theme
	fields = '__all__'


class topicCreate(CreateView):
	model = topic
	fields = ['topic_title', 'topic_description']

	def form_valid(self, form):
		form.instance.topic_theme_id = self.kwargs['pk']
		return super(topicCreate, self).form_valid(form)


class themeUpdate(UpdateView):
	model = theme
	fields = '__all__'


class topicUpdate(UpdateView):
	model = topic
	fields = ['topic_title', 'topic_description']


class themeDelete(DeleteView):
	model = theme
	success_url = reverse_lazy('repository:theme_index')

class topicDelete(DeleteView):
	model = topic

	def get_success_url(self):
		theme_info = topic.objects.get(pk=self.kwargs['pk']).topic_theme.id
		return reverse_lazy('repository:topic_index', kwargs={'pk':theme_info})
