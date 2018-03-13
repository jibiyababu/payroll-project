from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.employee_list, name='employee_list'),
    url(r'^employee/(?P<pk>\d+)/$', views.employee_detail, name='employee_detail'),
    url(r'^employee/new/$', views.employee_new, name='employee_new'),
    url(r'^employee/(?P<pk>\d+)/edit/$', views.employee_edit, name='employee_edit'),
]

