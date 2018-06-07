from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^employee/list$', views.employee_list, name='employee_list'),
    url(r'^employee/(?P<pk>\d+)/$', views.employee_detail, name='employee_detail'),
    url(r'^employee/new/$', views.employee_new, name='employee_new'),
    url(r'^employee/(?P<pk>\d+)/edit/$', views.employee_edit, name='employee_edit'),
    url(r'^admin/detail/$', views.admin_edit, name='admin_detail'),
    url(r'^employee/add/$', views.add_employee, name='add_employee'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate')
]

