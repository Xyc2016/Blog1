from django.conf.urls import url
from . import views
app_name = 'post'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<page>[0-9]+)/$', views.index, name='index'),
    url(r'^write/$', views.write, name='write'),
    url(r'^(?P<pk>[0-9]+)/detail',
        views.DetailView.as_view(), name='detail'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<article_id>[0-9]+)/add_comment/$',
        views.add_comment, name='add_comment'),
    url(r'^(?P<article_id>[0-9]+)/dlt_article/$',
        views.dlt_article, name='dlt_article'),
    url(r'^(?P<article_id>[0-9]+)/to_private', views.to_private, name='to_private'),
    url(r'^(?P<article_id>[0-9]+)/to_public', views.to_public, name='to_public'),
    url(r'^(?P<article_id>[0-9]+)/edit', views.edit, name='edit'),
    url(r'^(?P<page>[0-9]+)/all_articles', views.all_articles, name='all_articles'),
    url(r'^get_json/', views.get_json, name='get_json'),
]
