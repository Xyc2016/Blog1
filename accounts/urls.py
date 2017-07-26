from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^profile/$', views.profile, name='profile'),
]
