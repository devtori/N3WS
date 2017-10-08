from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result/(\w+)$', views.result, name='result'),
    url(r'^words/$', views.cloud, name='words'),
]
