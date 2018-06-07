from django.conf.urls import url
from django.conf.urls import include 
from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^employee/$', views.employee_detail, name='employee_detail'),
    url(r'^logout/$' , views.logout_view, name='logout'),
    url(r'signup/$' , views.admin_signup,name='signup')
]
