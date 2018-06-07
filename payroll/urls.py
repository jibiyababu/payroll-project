from django.conf.urls import url
from . import views
# from payroll.views import Pdf


urlpatterns = [
       url(r'^salary/(?P<pk>\d+)/$', views.salary_detail, name='salary_detail'),
       url(r'^salary-slip/(?P<pk>\d+)/$', views.salary_slip, name='salary_slip'),
    url(r'^salary/(?P<pk>\d+)/pdf/$',views.salary_pdf, name='salary_pdf'),
    
       url(r'^update-salary/(?P<pk>\d+)/$', views.update_salary, name='update_salary'),
           url(r'^update-salary/$', views.update_salary, name='update_salary'),
       url(r'^salary/view/$',views.salary_report,name='view_salary'),
       url(r'^salary/employee-list/$',views.salary_employee_list,name='salary_employee_list'),
       url(r'^salary/pending-list/$',views.salary_pending_list,name='salary_pending_list'),
    
]
