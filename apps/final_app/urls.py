from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^homepage$', views.homepage),
    url(r'^add$', views.add),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^poke/(?P<id>\d+)', views.poke),
]