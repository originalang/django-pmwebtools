from django.urls import path, re_path
from . import views

app_name = 'repository'

urlpatterns = [
	re_path(r'^topics/theme:(?P<pk>[0-9]+)/$', views.topic_index, name="topic_index"),
	path('themes/', views.theme_index, name="theme_index"),
	re_path(r'^topic:(?P<pk>[0-9]+)/$', views.topic_detail.as_view(), name='topic_detail'),
	path('theme/add/', views.themeCreate.as_view(), name='create-theme'),
	re_path(r'^theme/(?P<pk>[0-9]+)/delete/$', views.themeDelete.as_view(), name='delete-theme'),
	re_path(r'^theme/(?P<pk>[0-9]+)/update/$', views.themeUpdate.as_view(), name='update-theme'),
	re_path(r'^topic/(?P<pk>[0-9]+)/update/$', views.topicUpdate.as_view(), name='update-topic'),
	re_path(r'^topic/(?P<pk>[0-9]+)/add/$', views.topicCreate.as_view(), name='create-topic'),
	re_path(r'^topic/(?P<pk>[0-9]+)/delete/$', views.topicDelete.as_view(), name='delete-topic'),
]
