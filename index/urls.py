from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^account/$', views.account, name='account'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^investments/$', views.investments, name='investments'),
    url(r'^newlog/$', views.Createcapitallog.as_view(), name='createnewlog'),
    url(r'^newaccount/$', views.CapitalFlow.as_view(), name='capitalflow'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^forgetpass/$', views.forgetpassword, name='forgetpass'),
    url(r'^getacclogs/(?P<pk>[0-9]+)/$', views.AccountLog.as_view(), name='accountlog'),
    url(r'^$', views.index, name='index'),
]

urlpatterns = format_suffix_patterns(urlpatterns)