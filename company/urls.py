from django.conf.urls import url
from . import views

urlpatterns = [
           url(r'^company/$',views.edit_company,name='edit_company'),
           url(r'^holiday/$',views.add_holiday,name='add_holiday'),
           url(r'^work-type/$',views.add_worktype,name='add_worktype'),
           url(r'^designation/$',views.add_designation,name='add_designation'),
           url(r'^department/$',views.add_department,name='add_department'),
           url(r'^job-type/$',views.add_jobtype,name='add_jobtype'),
           url(r'^holiday/detail/$',views.holiday_detail,name='holiday_detail'),
           url(r'^holiday/(?P<pk>\d+)/$',views.holiday_delete,name='holiday_delete'),
           url(r'^work-type/detail/$',views.worktype_detail,name='worktype_detail'),
           url(r'^work-type/(?P<pk>\d+)/$',views.worktype_delete,name='worktype_delete'),
       url(r'^job-type/detail/$',views.jobtype_detail,name='jobtype_detail'),
       url(r'^job-type/(?P<pk>\d+)/$',views.jobtype_delete,name='jobtype_delete'),
    url(r'^department/detail/$',views.department_detail,name='department_detail'),
    url(r'^department/(?P<pk>\d+)/$',views.department_delete,name='department_delete'),
   
        url(r'^designation/detail/$',views.designation_detail,name='designation_detail'),
         url(r'^designation/(?P<pk>\d+)/$',views.designation_delete,name='designation_delete'),
       url(r'^company/home/$',views.company_homepage,name='company_homepage')
    
]
