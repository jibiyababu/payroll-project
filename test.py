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
