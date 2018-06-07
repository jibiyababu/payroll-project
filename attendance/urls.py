from django.conf.urls import url
from . import views

urlpatterns = [
           url(r'^attendance/$',views.new_mark_attendance,name='mark_attendance'),
           url(r'^attendance/(?P<pk>\d+)/$',views.mark_attendance,name='mark_attendance'),
           url(r'^attendance/view/$',views.view_attendance_employee,name='view_attendance'),
           url(r'^leave-application/$',views.leave_application,name='leave_application'),
           url(r'^attendance/view/company/$',views.view_attendance_company,name='view_attendance_company'),
    
           
]

        
