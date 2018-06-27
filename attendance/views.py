from django.shortcuts import render
from company.models import Holiday
from .models import Attendance,Leave_Application
from .forms import AttendanceForm, ViewAttendanceForm
from .forms import LeaveApplicationForm, ViewAttendanceCompanyForm
from user.forms import EmployeeForm
from user.models import Designation_History,Employee
from user.views import employee_detail
from company.models import Designation
from django.shortcuts import render,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.core.paginator import Paginator,PageNotAnInteger
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def new_mark_attendance(request):
    
    company=request.user.employee.company
    emp_count=Employee.objects.filter(company=company)
    print('emp_count',emp_count)
    data=[{
        'employee':emp
          }for emp in emp_count]
    
    AttendanceFormSet= formset_factory(AttendanceForm,max_num=1,can_order=True,can_delete=True)
    if request.method=="POST":
        form=ViewAttendanceCompanyForm(request.POST)
        Attendance_FormSet=AttendanceFormSet(request.POST)
        #attendance_form=AttendanceForm(request.POST)
        
        if Attendance_FormSet.is_valid():
            #attendance=Attendance_FormSet.save(commit=False)
            print('errors',Attendance_FormSet.errors)
            
            new_records=[]
            date=datetime.datetime.strptime(request.POST['monthdate'], "%Y-%m-%d")
            holiday=Holiday.objects.filter(date=date).exists()
            
            if not holiday and not date.weekday() == 5 and not date.weekday() == 6:

                for attendance_form in Attendance_FormSet:
                    print('attendance_Form',attendance_form)
                        

                    print('attendance',attendance_form.cleaned_data.get('employee'))
                    employee=attendance_form.cleaned_data.get('employee')
                    print('date & employee',date,employee)
                    attendance_exist=Attendance.objects.filter(employee=employee,date=date).exists()
                    print('attendance_Exist',attendance_exist)
                    if not attendance_exist:
                        print('employee',employee.pk)
                        date=request.POST['monthdate']
                        print(date)
                        mark=attendance_form.cleaned_data.get('mark')
                        print(mark)
                        leave_type=attendance_form.cleaned_data.get('leave_type')
                        print('leave-type',leave_type)
                        try:
                            last_record=Attendance.objects.filter(employee = employee.pk).latest('id')
                            print('last_Record',last_record)
                        except ObjectDoesNotExist:
                            last_record = None
                            print('last_Record',last_record)
                        try:
                        
                            dsgn=Designation_History.objects.filter(employee=employee.pk).latest('id')
                            print('dsgn-pl',dsgn.designation.privilege_leave)
                            if last_record: 
                                remPrivilegeLeave = last_record.remPrivilegeLeave
                                remCasualLeave = last_record.remCasualLeave
                                pl = last_record.pl
                                cl = last_record.cl
                                lop= last_record.lop
                                print('rempl',remPrivilegeLeave)
                        
                            else:
                                
                                remPrivilegeLeave = dsgn.designation.privilege_leave
                                remCasualLeave = dsgn.designation.casual_leave
                                pl=0
                                cl=0
                                lop=False
                                
                            if mark == 0 and leave_type =='Privilege Leave':
                                if last_record:
                                    if last_record.pl: 
                                        if last_record.pl>=dsgn.designation.privilege_leave:
                                            if last_record.cl<dsgn.designation.casual_leave:
                                                pl=last_record.pl
                                                cl=last_record.cl + 1
                                                remPrivilegeLeave = last_record.remPrivilegeLeave
                                                remCasualLeave = dsgn.designation.casual_leave - cl
                                            else:
                                                pl=last_record.pl
                                                cl=last_record.cl
                                                remPrivilegeLeave = last_record.remPrivilegeLeave
                                                remCasualLeave = last_record.remCasualLeave
                                                lop = True
                                        else:
                                            pl=last_record.pl + 1
                                            remPrivilegeLeave = dsgn.designation.privilege_leave - pl
                                            remCasualLeave = last_record.remCasualLeave
                                    
                                            if last_record.cl:
                                                cl=last_record.cl
                                   
                                    else:
                                        pl+=1
                                        remPrivilegeLeave = dsgn.designation.privilege_leave - pl
                                        remCasualLeave = last_record.remCasualLeave
                                        cl = last_record.cl
                    
                                else:
                                    pl+=1
                                    remPrivilegeLeave = dsgn.designation.privilege_leave - pl
                                    print('cl',dsgn.designation.casual_leave)
                                    remCasualLeave = dsgn.designation.casual_leave
                            
                           
                            if mark == 0 and leave_type=='Casual Leave':
                                if last_record:
                                    if last_record.cl:
                                        if last_record.cl >= dsgn.designation.casual_leave:
                                            if last_record.pl < dsgn.designation.privilege_leave:
                                                pl=last_record.pl + 1
                                                cl=last_record.cl
                                                remPrivilegeLeave = dsgn.designation.privilege_leave - pl
                                                remCasualLeave = last_record.remCasualLeave
                                            else:
                                                lop = True
                                                pl=last_record.pl
                                                cl=last_record.cl
                                                remPrivilegeLeave = last_record.remPrivilegeLeave
                                                remCasualLeave = last_record.remCasualLeave
                            
                                        else:
                                            cl=last_record.cl + 1
                                            remCasualLeave = dsgn.designation.casual_leave - cl
                                            remPrivilegeLeave = last_record.remPrivilegeLeave 
                                            if last_record.pl:
                                                pl=last_record.pl
                                    else:
                                        cl+=1
                                        remCasualLeave = dsgn.designation.casual_leave - cl
                                        remPrivilegeLeave = last_record.remPrivilegeLeave
                                        pl = last_record.pl 
                                else:
                                    cl+=1
                                    remCasualLeave = dsgn.designation.casual_leave - cl
                                    remPrivilegeLeave = dsgn.designation.privilege_leave

                                
                    
                            print('employee',employee)
                            print('date',date)
                            print('mark',mark)
                            print('leave_Type',leave_type)
                            print('remPrivilegeLeave',remPrivilegeLeave)
                            print('remCasualLeave',remCasualLeave)
                            print('pl',pl)
                            print('cl',cl)
                            print('lop',lop)
                            # if not lop:
                            #     lop=False
                        
                            new_records.append(Attendance(
                                employee=employee,
                                date=date,
                                mark=mark,
                                leave_type=leave_type,
                                remPrivilegeLeave=remPrivilegeLeave,
                                remCasualLeave=remCasualLeave,
                                pl=pl,
                                cl=cl,
                                lop=lop
                            ))
                        
                            print('new_Records',new_records)
                            
                        except ObjectDoesNotExist:
                            messages.success(request,'Please complete employee profile before mark attendance !!')
                            return redirect('mark_attendance')
                    else:
                        messages.success(request,'Attendance has marked for %s'%(employee))
                try:
                        
                    Attendance.objects.bulk_create(new_records)
                    messages.success(request,'Record created !')
                    return redirect('mark_attendance')
                except:
                    messages.success(request,'Bulk_create error !')
                    return redirect('mark_attendance')
            else:
                messages.success(request,'Attendance cannot be marked on holiday!')
                return redirect('mark_attendance')
        
            
        else:
            messages.success(request,'Invalid details !')
            return redirect('mark_attendance')
    else:
        #attendance_form=AttendanceForm(company=company)
        form=ViewAttendanceCompanyForm({'monthdate':datetime.datetime.now().date()})
        Attendance_FormSet=AttendanceFormSet(form_kwargs={'company':company})
        #formset = ArticleFormSet(form_kwargs={'user': request.user})
    return render(request,
                  'attendance/new_mark_attendance.html',
                  {
                      'Attendance_FormSet':Attendance_FormSet,
                      'form':form                
                  }
    )


def mark_attendance(request,pk=None):
    data={
        'date':datetime.datetime.now().date(),
        'employee':pk 
    }
    company=request.user.employee.company

    if request.method=="POST":
        
        form=AttendanceForm(request.POST)
        
        print('form',form)
        print('form is valid',form.is_valid())
        print('errors')
        
        if form.is_valid():
            if not pk:
                pk=request.POST['employee']
                attendance=Attendance.objects.filter(date=datetime.datetime.now().date(),employee=pk).annotate(Count('id'))
                employee=form.cleaned_data.get('employee')
                print('emp',employee.pk)
                
            if not attendance.exists(): # only one record entry is allowed
                leave=request.POST['leave_type']
                print('leave=',leave)

                try:
                    last_record=Attendance.objects.filter(employee = pk).latest('id')
                    
                except:
                    last_record = None
                    print('employee:',pk)
                    print('last_record',last_record)
                    
                try:
                    dsgn=Designation_History.objects.filter(employee=pk).latest('id')
                    print('dsgn',dsgn.designation.privilege_leave)
                    print('dsgn',dsgn.designation.casual_leave)
                    
                
                    record=form.save(commit=False)

                    if last_record: 
                        record.remPrivilegeLeave = last_record.remPrivilegeLeave
                        record.remCasualLeave = last_record.remCasualLeave
                        record.pl = last_record.pl
                        record.cl = last_record.cl
                        
                    else:
                        record.remPrivilegeLeave = dsgn.designation.privilege_leave
                        record.remCasualLeave = dsgn.designation.casual_leave

                    if leave_type =='Privilege Leave':
                        if last_record:
                            if last_record.pl: 
                                if last_record.pl>=dsgn.designation.privilege_leave:
                                   if last_record.cl<dsgn.designation.casual_leave:
                                       record.pl=last_record.pl
                                       record.cl=last_record.cl + 1
                                       record.remPrivilegeLeave = last_record.remPrivilegeLeave
                                       record.remCasualLeave = dsgn.designation.casual_leave - record.cl

                                   else:
                                       record.pl=last_record.pl
                                       record.cl=last_record.cl
                                       record.remPrivilegeLeave = last_record.remPrivilegeLeave
                                       record.remCasualLeave = last_record.remCasualLeave
                                       record.lop = True

                                else:
                                    record.pl=last_record.pl + 1
                                    record.remPrivilegeLeave = dsgn.designation.privilege_leave - record.pl
                                    record.remCasualLeave = last_record.remCasualLeave
                                    print('pl=',record.pl)
                                    if last_record.cl:
                                        record.cl=last_record.cl

                            else:
                                record.pl+=1
                                record.remPrivilegeLeave = dsgn.designation.privilege_leave - record.pl
                                record.remCasualLeave = last_record.remCasualLeave
                                record.cl = last_record.cl
                                
                        else:
                            record.pl+=1
                            record.remPrivilegeLeave = dsgn.designation.privilege_leave - record.pl
                            print('cl',dsgn.designation.casual_leave)
                            record.remCasualLeave = dsgn.designation.casual_leave
                            
                           
                    if leave=='Casual Leave':
                        if last_record:
                            if last_record.cl:
                                if last_record.cl >= dsgn.designation.casual_leave:
                                    if last_record.pl < dsgn.designation.privilege_leave:
                                        record.pl=last_record.pl + 1
                                        record.cl=last_record.cl
                                        record.remPrivilegeLeave = dsgn.designation.privilege_leave - record.pl
                                        record.remCasualLeave = last_record.remCasualLeave
                                    else:
                                        record.lop = True
                                        record.pl=last_record.pl
                                        record.cl=last_record.cl
                                        record.remPrivilegeLeave = last_record.remPrivilegeLeave
                                        record.remCasualLeave = last_record.remCasualLeave
                                        
                                else:
                                    record.cl=last_record.cl + 1
                                    record.remCasualLeave = dsgn.designation.casual_leave - record.cl
                                    record.remPrivilegeLeave = last_record.remPrivilegeLeave 
                                    if last_record.pl:
                                        record.pl=last_record.pl
                                        
                            else:
                                record.cl+=1
                                record.remCasualLeave = dsgn.designation.casual_leave - record.cl
                                record.remPrivilegeLeave = last_record.remPrivilegeLeave
                                record.pl = last_record.pl 
                        else:
                            record.cl+=1
                            record.remCasualLeave = dsgn.designation.casual_leave - record.cl
                            record.remPrivilegeLeave = dsgn.designation.privilege_leave
                            
                    record.save()
                    record.refresh_from_db()
                    messages.success(request,'Attendance marked successfully')
                    return redirect('mark_attendance')
                except:
                    messages.success(request,'Please complete employee profile before mark attendance !!')
                    return redirect('employee_detail',pk=pk)
            else:
                messages.success(request,'Attendance cannot be marked again !!')
                return redirect('mark_attendance')
        else:
            messages.success(request,"invalid credentials")
            return redirect('mark_attendance')
    else:
        
        form = AttendanceForm(company=company,initial=data)
        emp=form['employee']
        #print('form.employee:')
        record = Attendance.objects.filter(date=datetime.datetime.now())
        print('record',record)
    return render(request,'attendance/mark_attendance.html',{'form':form,'record':record })

def view_attendance_employee(request):
    company=request.user.employee.company
    if request.method=="POST":
        form=ViewAttendanceForm(request.POST)
        print('employee',form['employee'])
        print('start-date',request.POST['start_date'])
        print('end-date',request.POST['end_date'])
        print('form valid',form.is_valid())
        print('form bound',form.is_bound)
        if form.is_valid():
            emp_id=request.POST['employee']
            print(emp_id)
            print(type(request.POST['start_date']))
            print(request.POST['end_date'])
            mark=request.POST['mark']
            records=Attendance.objects.filter(employee = emp_id,mark=mark, date__range=[request.POST['start_date'],request.POST['end_date']])
            print('records',records)
            
            return render(request,'attendance/view_attendance.html',{'form':form,'records':records})
        #return redirect('view_attendance_employee',{'records':records})
        else:
            messages.success(request,'Invalid Details !')
            return redirect('view_attendance')
    else:
        form=ViewAttendanceForm(company=company)
        
    return render(request,'attendance/view_attendance.html',{'form':form })

def view_attendance_company(request):
    date=datetime.datetime.now().date()
    data={
        'monthdate':date
    }
    company=request.user.employee.company
    if request.method=="POST":

        form=ViewAttendanceCompanyForm(request.POST)
        print('date:',request.POST['monthdate'])
        if form.is_valid():
            date=request.POST['monthdate']
            emp_count=Employee.objects.filter(company=company)
            try:
                records=Attendance.objects.filter(employee__in=emp_count,date=date)
                
            except ObjectDoesNotExist:
                records=None
                
                 
            #messages.success(request,'Valid Credentials')
            return render(request,'attendance/view_attendance_company.html',{'form':form,'records':records,'date':date})
        else:
            messages.success(request,'Invalid Details !')
            return redirect('view_attendance_company')
        
            
            
    else:
        form=ViewAttendanceCompanyForm(initial=data)
        emp_count=Employee.objects.filter(company=company)
        try:
            records=Attendance.objects.filter(employee__in=emp_count,date=date)
            
        except ObjectDoesNotExist:
            records=None
            
    return render(request,'attendance/view_attendance_company.html',{'form':form,'records':records,'date':date})        

















def leave_application(request):
    user=request.user.employee
    leave=Attendance.objects.filter(employee=user)
    if request.method=="POST":
        form=LeaveApplicationForm(request.POST)
        leaveapplication=Leave_Application.objects.filter(employee=request.user.employee)
        if form.is_valid():
            leaveform= form.save()
            messages.success(request,'Valid Credentials')
            return render(request,'attendance/leaveapplication_detail.html',{'leaveapplication':leaveapplication,'leave':leave})
        else:
            messages.success(request,'Invalid Details !')
            return redirect('leave_application')
    else:
        form=LeaveApplicationForm()
    return render(request,'attendance/leave_application.html',{'form':form,'leave':leave })

