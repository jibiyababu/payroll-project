from django.shortcuts import render
from .models import Attendance,Leave_Application
from .forms import AttendanceForm, ViewAttendanceForm
from .forms import LeaveApplicationForm, ViewAttendanceCompanyForm
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
from django.core.paginator import Paginator,PageNotAnInteger
import datetime
# Create your views here.

def new_mark_attendance(request):
    
    company=request.user.employee.company
    emp_count=Employee.objects.filter(company=company)
    attendance_record=Attendance.objects.filter(employee__in=emp_count,date=datetime.datetime.now().date())
    print(emp_count)
    data=[{
        'employee':emp
          }for emp in emp_count]
    
    AttendanceFormSet = formset_factory(AttendanceForm,max_num=1)

    
    if request.method=="POST":
        form=ViewAttendanceCompanyForm(request.POST)
        Attendance_FormSet=AttendanceFormSet(request.POST)
    
        if Attendance_FormSet.is_valid():
            
            #attendance_record=Attendance.objects.filter(employee__in=emp_count,date=datetime.datetime.now().date()).exists()
            
            print('attendance_record',attendance_record)
            if not False:
                # attendance_record:
                new_records=[]
                for Attendance_Form in Attendance_FormSet:
                    employee=Attendance_Form.cleaned_data.get('employee')
                    print('employee',employee)
                    date=request.POST['monthdate']
                    
                    mark=Attendance_Form.cleaned_data.get('mark')
                
                    leave_type=Attendance_Form.cleaned_data.get('leave_type')
                    print('leave-type',leave_type)
                    try:
                        last_record=Attendance.objects.filter(employee = employee.pk).latest('id')
                        print('last_Record',last_record)
                    except ObjectDoesNotExist:
                        last_record = None
                   
                    try:
                    
                        dsgn=Designation_History.objects.filter(employee=employee.pk).latest('id')
                        print('dsgn-pl',dsgn.designation.privilege_leave)
                        if last_record: 
                            remPrivilegeLeave = last_record.remPrivilegeLeave
                            remCasualLeave = last_record.remCasualLeave
                            pl = last_record.pl
                            cl = last_record.cl
                            print('rempl',remPrivilegeLeave)
                            
                        else:
                            
                            remPrivilegeLeave = dsgn.designation.privilege_leave
                            remCasualLeave = dsgn.designation.casual_leave
                            print('rempl',remPrivilegeLeave)

                                        
                    


                        print('employee',employee)
                        print('date',date)
                        print('mark',mark)
                        print('leave_Type',leave_type)
                        print('remPrivilegeLeave',remPrivilegeLeave)
                        print('remCasualLeave',remCasualLeave)
                        # print('pl',pl)
                        # print('cl',cl)
                        #if employee and date and mark  and remPrivilegeLeave and remCasualLeave :
                        # if not lop:
                        #     lop=False
                    
                        new_records.append(Attendance(
                            employee=employee,
                            date=date,
                            mark=mark,
                            leave_type=leave_type,
                            remPrivilegeLeave=remPrivilegeLeave,
                            remCasualLeave=remCasualLeave,
                            
                        ))
                        print('new_Records',new_records)
                    # if pl and cl:
                    #     new_records.append(Attendance(
                    #     employee=employee,
                    #     date=date,
                    #     mark=mark,
                    #     leave_type=leave_type,
                    #     remPrivilegeLeave=remPrivilegeLeave,
                    #     remCasualLeave=remCasualLeave,
                    #     pl=pl,
                    #     cl=cl
                    # ))
                        
                    
                
                    except:
                        messages.success(request,'Please complete employee profile before mark attendance !!')
                        return redirect('mark_attendance')
            
                try:
                    print('new_Records',new_records)
                    Attendance.objects.bulk_create(new_records)
                    messages.success(request,'Record created !')
                    return redirect('mark_attendance')
                except:
                    messages.success(request,'Bulk_create error !')
                    return redirect('mark_attendance')
            else:
                messages.success(request,'Attendance has already marked !')
                return redirect('mark_attendance')
        else:
            messages.success(request,'Invalid details !')
            return redirect('mark_attendance')
    else:

        # query=Employee.objects.filter(company=company)
        # paginator = Paginator(query, 5)  # Show 10 forms per page
        # page = request.GET.get('page')
        # try:
        #     objects = paginator.page(page)
        # except PageNotAnInteger:
        #     objects = paginator.page(1)
        # except EmptyPage:
        #     objects = paginator.page(paginator.num_pages)
        # page_query = Employee.objects.filter(id__in=[object.id for object in objects])
        #formset = FormSet(queryset=page_query)
                                        


        
        form=ViewAttendanceCompanyForm({'monthdate':timezone.now()})
        Attendance_FormSet=AttendanceFormSet(initial=data)
    return render(request,'attendance/new_mark_attendance.html',{'Attendance_FormSet':Attendance_FormSet,'form':form})


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
            records=Attendance.objects.filter(employee = emp_id, date__range=[request.POST['start_date'],request.POST['end_date']])
            print('records',records)
            messages.success(request,'Valid Credentials')
            return render(request,'attendance/attendance_detail.html',{'records':records})
        #return redirect('view_attendance_employee',{'records':records})
        else:
            messages.success(request,'Invalid Details !')
            return redirect('view_attendance')
    else:
        form=ViewAttendanceForm()
        
    return render(request,'attendance/view_attendance.html',{'form':form })

def view_attendance_company(request):
    date=datetime.datetime.now().date()
    data={
        'monthdate':date
    }
    if request.method=="POST":

        form=ViewAttendanceCompanyForm(request.POST)
        print('date:',request.POST['monthdate'])
        if form.is_valid():
            date=request.POST['monthdate']
            emp_count=Employee.objects.filter(company=16)
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
        emp_count=Employee.objects.filter(company=16)
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

