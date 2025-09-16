from django.shortcuts import render, redirect, get_object_or_404
from adminApp.models import *
from django.contrib import messages
from customUserAuth.models import *
from adminApp.models import *
from employeeApp.models import *
from adminApp.forms import *
from employeeApp.forms import *
from django.contrib.auth.decorators import login_required
from adminApp.forms import PromotionModelForm, ResignationModelForm, TerminationModelForm
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .middleware import ActivityLoggingMiddleware
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, date
import calendar
import requests
from django.utils.timezone import now

# Create your views here.
@login_required
def dashboard(request):
    today = timezone.now().date()

    # Existing stats...
    total_employees = ProfileModel.objects.count()
    total_departments = DepartmentModel.objects.count()
    total_designations = DesignationModel.objects.count()

    # Recent notices
    recent_notices = NoticeModel.objects.filter(is_active=True).order_by('-created_at')[:5]

    # Upcoming holidays
    upcoming_holidays = HolidayModel.objects.filter(date__gte=today).order_by('date')[:5]

    # Department statistics
    department_stats = DepartmentModel.objects.annotate(
        employee_count=Count('department_info__designation_info')
    ).values('name', 'employee_count')

    # Recent activities
    recent_activities = ActivityLogModel.objects.select_related('user').order_by('-timestamp')[:5]

    # Today's holiday
    today_holiday = HolidayModel.objects.filter(date=today).first()

    # New employees
    new_employees = ProfileModel.objects.filter(
        date_of_joining__gte=today - timezone.timedelta(days=30)
    ).count()
    new_employee_percentage = round((new_employees / total_employees) * 100) if total_employees > 0 else 0

    # All employee tasks
    assigned_tasks = TaskModel.objects.select_related('assigned_to', 'assigned_by').order_by('-due_date')

    # Task status counts
    task_status_counts = {
        'pending': TaskModel.objects.filter(status='pending').count(),
        'in_progress': TaskModel.objects.filter(status='in_progress').count(),
        'completed': TaskModel.objects.filter(status='completed').count(),
    }

    # ===== Leave statistics =====
    leave_counts = {
        'approved': LeaveRequestModel.objects.filter(status='approved').count(),
        'pending': LeaveRequestModel.objects.filter(status='pending').count(),
        'rejected': LeaveRequestModel.objects.filter(status='rejected').count(),
    }

    # ===== Attendance (today) =====
    present_count = AttendanceModel.objects.filter(date=today, status='present').count()
    absent_count = AttendanceModel.objects.filter(date=today, status='absent').count()

    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_designations': total_designations,
        'recent_notices': recent_notices,
        'upcoming_holidays': upcoming_holidays,
        'department_stats': department_stats,
        'recent_activities': recent_activities,
        'today_holiday': today_holiday,
        'new_employees': new_employees,
        'new_employee_percentage': new_employee_percentage,
        'assigned_tasks': assigned_tasks,
        'task_status_counts': task_status_counts,
        'leave_counts': leave_counts,                 
        'present_count': present_count,               
        'absent_count': absent_count,                
    }

    return render(request, 'dashboard.html', context)


@login_required
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = TaskModel.objects.get(id=task_id)
        if task.assigned_to == request.user.profile:
            new_status = request.POST.get('status')
            if new_status in ['pending', 'in_progress', 'completed']:
                task.status = new_status
                task.save()
    return redirect('dashboard')

@login_required
def profile_view(request):
    profile, created = ProfileModel.objects.get_or_create(user=request.user)

    team_member = TeamMemberModel.objects.filter(member=profile).first()

    is_team_lead = TeamMemberModel.objects.filter(
        member__user=request.user, 
        role="Lead"
    ).exists()

    context = {
        'profile': profile,
        'team_member': team_member,
        'is_team_lead': is_team_lead,
    }
    return render(request, 'profile.html', context)

@login_required
def update_profile(request):
    profile = request.user.profile  # Assuming OneToOne relation
    user = request.user

    if request.method == 'POST':
        try:
            # Update user email
            email = request.POST.get('email', '').strip()
            if email and email != user.email:
                if CustomUserAuthModel.objects.filter(email=email).exclude(id=user.id).exists():
                    messages.error(request, "This email is already taken.")
                    return redirect('update_profile')
                user.email = email
                user.username = email  # Keep username in sync
                user.save()

            # Update profile fields
            profile.full_name = request.POST.get('full_name', '').strip()
            profile.phone = request.POST.get('phone', '').strip()
            profile.address = request.POST.get('address', '').strip()
            profile.gender = request.POST.get('gender', '').strip()
            
            birthday = request.POST.get('birthday')
            if birthday:
                profile.birthday = birthday

            date_of_joining = request.POST.get('date_of_joining')
            if date_of_joining:
                profile.date_of_joining = date_of_joining

            position_id = request.POST.get('position')
            if position_id:
                try:
                    profile.position = DesignationModel.objects.get(id=position_id)
                except DesignationModel.DoesNotExist:
                    profile.position = None

            reports_to_id = request.POST.get('reports_to')
            if reports_to_id:
                try:
                    profile.reports_to = ProfileModel.objects.get(id=reports_to_id)
                except ProfileModel.DoesNotExist:
                    profile.reports_to = None

            # Handle profile image
            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                if profile_image.content_type.startswith('image/'):
                    profile.profile_image = profile_image
                else:
                    messages.error(request, "Please upload a valid image file.")
                    return redirect('update_profile')

            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('my_profile')

        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")
            return redirect('update_profile')

    # For GET requests
    positions = DesignationModel.objects.all()
    managers = ProfileModel.objects.exclude(id=profile.id)

    context = {
        'profile': profile,
        'positions': positions,
        'managers': managers,
    }
    return render(request, 'update_profile.html', context)

@login_required
def update_team_member_role(request, pk):
    team_member = get_object_or_404(TeamMemberModel, pk=pk)

    # Only allow team lead or admin to update
    if request.user.user_types not in ['Admin'] and not team_member.role == 'Lead':
        return redirect('profile')

    if request.method == "POST":
        role = request.POST.get('role')
        if role in ['Lead', 'Member']:
            team_member.role = role
            team_member.save()
    return redirect('profile')

@login_required
def view_profile(request, user_id):
    profile = get_object_or_404(ProfileModel, user__id=user_id)
    context = {'profile': profile}
    return render(request, 'profile.html', context)

#Department
@login_required
def addDepartment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name:
            DepartmentModel.objects.create(
                name = name,
                description = description,
            )
            messages.success(request, 'Department added successfully!')
            return redirect('departments')
        else:
            messages.error(request, 'Department name is required!')
    
    return redirect('departments')

@login_required
def departments(request):
    departments = DepartmentModel.objects.all().order_by('id')
    return render(request, 'departments/departments.html',{'departments':departments})

@login_required
def editDepartment(request, dept_id):
    department = DepartmentModel.objects.get(id=dept_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            department.name = name
            department.description = description
            department.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('departments')
        else:
            messages.error(request, 'Department name is required!')
    
    context = {
        'department': department,
    }
    return render(request, 'departments/editDepartment.html', context)


@login_required
def deleteDepartment(request, dept_id):
    department = DepartmentModel.objects.get(id=dept_id)
    
    if request.method == 'POST':
        if department.department_info.exists():
            messages.error(request, 'Cannot delete department with existing designations!')
            return redirect('departments')
        
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('departments')
    
    context = {
        'department': department,
    }
    return render(request, 'departments/deleteDepartment.html', context)


#Designation
@login_required
def designation_list(request):
    designations = DesignationModel.objects.select_related('department').all().order_by('department__name', 'title')
    departments = DepartmentModel.objects.all()
    
    context = {
        'designations': designations,
        'departments': departments,
    }
    return render(request, 'departments/designations.html', context)

@login_required
def add_designation(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        department_id = request.POST.get('department')
        
        if title and department_id:
            try:
                department = DepartmentModel.objects.get(id=department_id)
                DesignationModel.objects.create(
                    title=title,
                    department=department
                )
                messages.success(request, 'Designation added successfully!')
                return redirect('designation_list')
            except DepartmentModel.DoesNotExist:
                messages.error(request, 'Invalid department selected!')
        else:
            messages.error(request, 'Title and Department are required!')
    
    return redirect('designation_list')

@login_required
def edit_designation(request, desig_id):
    designation = get_object_or_404(DesignationModel, id=desig_id)
    departments = DepartmentModel.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        department_id = request.POST.get('department')
        
        if title and department_id:
            try:
                department = DepartmentModel.objects.get(id=department_id)
                designation.title = title
                designation.department = department
                designation.save()
                messages.success(request, 'Designation updated successfully!')
                return redirect('designation_list')
            except DepartmentModel.DoesNotExist:
                messages.error(request, 'Invalid department selected!')
        else:
            messages.error(request, 'Title and Department are required!')
    
    context = {
        'designation': designation,
        'departments': departments,
    }
    return render(request, 'departments/edit_designation.html', context)

@login_required
def delete_designation(request, desig_id):
    designation = get_object_or_404(DesignationModel, id=desig_id)
    
    if request.method == 'POST':
        if designation.designation_info.exists():
            messages.error(request, 'Cannot delete designation with existing employees!')
            return redirect('designation_list')
        
        designation.delete()
        messages.success(request, 'Designation deleted successfully!')
        return redirect('designation_list')
    
    context = {
        'designation': designation,
    }
    return render(request, 'departments/delete_designation.html', context)

#Employees

User = get_user_model()

@login_required
def add_employee(request):
    positions = DesignationModel.objects.all()
    managers = ProfileModel.objects.all().order_by('full_name')

    # Generate a random password for the new employee
    auto_password = get_random_string(length=8)

    # Generate next employee ID like EMP-001, EMP-002
    last_employee = ProfileModel.objects.order_by('id').last()
    if last_employee and last_employee.employee_id:
        try:
            last_id = int(last_employee.employee_id.split('-')[-1])
            next_employee_id = f"EMP-{last_id + 1:03d}"
        except ValueError:
            next_employee_id = "EMP-001"
    else:
        next_employee_id = "EMP-001"

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password") or auto_password
        employee_id = request.POST.get("employee_id") or next_employee_id
        date_of_joining = request.POST.get("date_of_joining")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        birthday = request.POST.get("birthday")
        address = request.POST.get("address")
        profile_image = request.FILES.get("profile_image")

        # Safely convert optional foreign keys
        position_id = request.POST.get("position")
        position_id = int(position_id) if position_id else None

        reports_to_id = request.POST.get("reports_to")
        reports_to_id = int(reports_to_id) if reports_to_id else None

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("add_employee")

        # Create employee user automatically as staff
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            user_types = 'Employee',
            is_staff=True,
            is_superuser=False
        )

        # Create employee profile
        ProfileModel.objects.create(
            user=user,
            full_name=full_name,
            employee_id=employee_id,
            position_id=position_id,
            date_of_joining=date_of_joining or None,
            phone=phone,
            gender=gender,
            birthday=birthday or None,
            address=address,
            profile_image=profile_image,
            reports_to_id=reports_to_id
        )

        messages.success(request, f"Employee '{full_name}' created successfully. Password: {password}")
        return redirect("employeeList")

    return render(request, "add_employee.html", {
        "positions": positions,
        "managers": managers,
        "auto_password": auto_password,
        "next_employee_id": next_employee_id
    })

@login_required
def add_admin(request):
    auto_password = get_random_string(length=10)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password") or auto_password
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("add_admin")

        user = User.objects.create_user(
            username=email,
            email=email,
            user_types = 'Admin',
            password=password,
        )

        ProfileModel.objects.create(
            user=user,
            full_name=full_name,
            employee_id=f"ADM-{user.id:03d}",  
            position=None,  
            date_of_joining=None,
            phone="",
            gender="",
            birthday=None,
            address="",
        )

        messages.success(request, f"Admin '{full_name}' created successfully. Password: {password}")
        return redirect("dashboard")  

    return render(request, "add_admin.html", {
        "auto_password": auto_password,
    })

@login_required
def employeeList(request):
    employees = ProfileModel.objects.all()
    designations = DesignationModel.objects.all()
    
    context = {
        'employees': employees,
        'designations': designations,
    }
    return render(request, 'employees.html', context)

@login_required
def employeeListView(request):
    employees = ProfileModel.objects.all()
    designations = DesignationModel.objects.all()
    
    context = {
        'employees': employees,
        'designations': designations,
    }
    return render(request, 'employees-list.html',context)

@login_required
def edit_profile(request, pk):
    profile = get_object_or_404(ProfileModel, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('employeeList')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})

@login_required
def delete_employee(request, pk):
    profile = get_object_or_404(ProfileModel, pk=pk)
    profile.delete()
    return redirect('employeeList')

#Leaves
@login_required
def addLeave(request):
    employees = ProfileModel.objects.all()
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        employee = get_object_or_404(ProfileModel, id=employee_id)
        LeaveRequestModel.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        messages.success(request, "Leave request created successfully.")
        return redirect('leaves_list')

    context = {'employees': employees}
    return redirect('leavesList',context)

@login_required
def leavesList(request):
    today = timezone.now().date()

    # Get all leave requests
    leave_requests = LeaveRequestModel.objects.select_related(
        'employee__user', 'employee__position'
    ).order_by('-applied_at')

    # Calculate statistics
    total_employees = ProfileModel.objects.count()

    # Leaves for today
    leaves_today = leave_requests.filter(start_date__lte=today, end_date__gte=today)
    planned_leaves_today = leaves_today.filter(status='planned').count()
    unplanned_leaves_today = leaves_today.filter(status='unplanned').count()
    pending_requests = leave_requests.filter(status='pending').count()

    if request.method == "POST":
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')
        leave = get_object_or_404(LeaveRequestModel, id=leave_id)
        leave.status = action
        leave.actioned_by = request.user.profile
        leave.actioned_at = timezone.now()
        leave.save()
        messages.success(request, f"Leave {action} successfully.")
        return redirect('leavesList')

    context = {
        'leave_requests': leave_requests,
        'total_employees': total_employees,
        'planned_leaves_today': planned_leaves_today,
        'unplanned_leaves_today': unplanned_leaves_today,
        'pending_requests': pending_requests,
    }
    return render(request, 'leaves.html', context)

@login_required
def leave_requests_admin_view(request):
    leave_requests = LeaveRequestModel.objects.all().order_by('-applied_at')

    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')
        leave = get_object_or_404(LeaveRequestModel, id=leave_id)
        leave.status = action
        leave.actioned_by = request.user.profile
        leave.actioned_at = timezone.now()
        leave.save()
        return redirect('admin_leave_requests')

    context = {
        'leave_requests': leave_requests,
    }
    return render(request, 'admin_leave_requests.html', context)

#attendance
@login_required
def attendanceDashboard(request):
    user = request.user

    # Fetch attendances
    if user.user_types == 'Admin':
        attendances = AttendanceModel.objects.select_related('employee').all().order_by('-date')
    else:
        attendances = AttendanceModel.objects.filter(employee__user=user).order_by('-date')

    today_date = now().date()

    # Today's hours
    today_attendance = attendances.filter(date=today_date).first()
    today_hours = today_attendance.work_duration if today_attendance else 0

    # Weekly hours
    start_week = today_date - timedelta(days=today_date.weekday())
    end_week = start_week + timedelta(days=6)
    week_attendances = attendances.filter(date__range=[start_week, end_week])
    week_hours = sum([att.work_duration or 0 for att in week_attendances])

    # Monthly hours
    start_month = today_date.replace(day=1)
    month_attendances = attendances.filter(date__gte=start_month)
    month_hours = sum([att.work_duration or 0 for att in month_attendances])

    # Total overtime
    total_overtime = sum([att.overtime or 0 for att in attendances])

    # Monthly summary
    total_days_in_month = calendar.monthrange(today_date.year, today_date.month)[1]
    total_present = month_attendances.filter(status="Present").count()
    total_absent = month_attendances.filter(status="Absent").count()
    total_late = month_attendances.filter(status="Late").count()

    present_summary = f"{total_present:02d}/{total_days_in_month:02d}"
    absent_summary = f"{total_absent:02d}/{total_days_in_month:02d}"
    late_summary = f"{total_late:02d}/{total_days_in_month:02d}"

    # Stats for progress bars
    stats = [
        {'label': 'Today', 'hours': today_hours or 0, 'max_hours': 8},
        {'label': 'This Week', 'hours': week_hours or 0, 'max_hours': 40},
        {'label': 'This Month', 'hours': month_hours or 0, 'max_hours': 160},
        {'label': 'Overtime', 'hours': total_overtime or 0, 'max_hours': 20},
    ]
    for stat in stats:
        stat['percentage'] = (stat['hours'] / stat['max_hours'] * 100) if stat['max_hours'] else 0

    context = {
        'attendances': attendances,
        'today_date': today_date,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_late': total_late,
        'present_summary': present_summary,
        'absent_summary': absent_summary,
        'late_summary': late_summary,
        'stats': stats,
    }
    return render(request, 'attendanceDashboard.html')

@login_required
def attendance(request):
    user = request.user

    # If admin, show all employees, else only current user's
    if hasattr(user, "user_types") and user.user_types == 'Admin':
        attendances = AttendanceModel.objects.select_related('employee').all().order_by('-date')
        employees = ProfileModel.objects.all()
    else:
        attendances = AttendanceModel.objects.filter(employee__user=user).order_by('-date')
        employees = ProfileModel.objects.filter(user=user)

    today_date = now().date()

    # Today's hours
    today_attendance = attendances.filter(date=today_date).first()
    today_hours = today_attendance.work_duration if today_attendance else 0

    # Weekly hours
    start_week = today_date - timedelta(days=today_date.weekday())
    end_week = start_week + timedelta(days=6)
    week_attendances = attendances.filter(date__range=[start_week, end_week])
    week_hours = sum([att.work_duration or 0 for att in week_attendances])

    # Monthly hours
    start_month = today_date.replace(day=1)
    month_attendances = attendances.filter(date__gte=start_month)
    month_hours = sum([att.work_duration or 0 for att in month_attendances])

    # Total overtime
    total_overtime = sum([att.overtime or 0 for att in attendances])

    # Monthly summary
    total_days_in_month = calendar.monthrange(today_date.year, today_date.month)[1]
    total_present = month_attendances.filter(status="Present").count()
    total_absent = month_attendances.filter(status="Absent").count()
    total_late = month_attendances.filter(status="Late").count()

    present_summary = f"{total_present:02d}/{total_days_in_month:02d}"
    absent_summary = f"{total_absent:02d}/{total_days_in_month:02d}"
    late_summary = f"{total_late:02d}/{total_days_in_month:02d}"

    # Stats for progress bars
    stats = [
        {'label': 'Today', 'hours': today_hours or 0, 'max_hours': 8},
        {'label': 'This Week', 'hours': week_hours or 0, 'max_hours': 40},
        {'label': 'This Month', 'hours': month_hours or 0, 'max_hours': 160},
        {'label': 'Overtime', 'hours': total_overtime or 0, 'max_hours': 20},
    ]
    for stat in stats:
        stat['percentage'] = (stat['hours'] / stat['max_hours'] * 100) if stat['max_hours'] else 0

    # Days in current month
    days = range(1, total_days_in_month + 1)

    # Attendance map for each employee
    attendance_map = {}
    for emp in employees:
        emp_attendance = AttendanceModel.objects.filter(
            employee=emp,
            date__year=today_date.year,
            date__month=today_date.month
        )
        emp_days = {att.date.day: att for att in emp_attendance}
        attendance_map[emp.id] = emp_days

    context = {
        'attendances': attendances,
        'employees': employees,
        'attendance_map': attendance_map,
        'days': days,
        'today_date': today_date,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_late': total_late,
        'present_summary': present_summary,
        'absent_summary': absent_summary,
        'late_summary': late_summary,
        'stats': stats,
    }
    return render(request, 'attendance.html', context)

#Holidays
# @login_required
# def holiday_list(request):
#     current_year = timezone.now().year
#     year = int(request.GET.get('year', current_year))
#     holidays = HolidayModel.objects.filter(date__year=year).order_by('date')
    
#     years = list(range(current_year - 5, current_year + 6))
    
#     context = {
#         'holidays': holidays,
#         'current_year': year,
#         'years': years,
#     }
#     return render(request, 'holidays.html', context)


@login_required
def holiday_list(request):
    current_year = timezone.now().year
    year = int(request.GET.get('year', current_year))

    # Fetch holidays from DB
    holidays = HolidayModel.objects.filter(date__year=year).order_by('date')

    # Add Bangladesh public holidays automatically if not exists
    try:
        response = requests.get(f'https://date.nager.at/api/v3/PublicHolidays/{year}/BD')
        if response.status_code == 200:
            bh_holidays = response.json()
            for h in bh_holidays:
                # Extract only the date part YYYY-MM-DD
                date_str = h['date'].split('T')[0]
                if not HolidayModel.objects.filter(date=date_str).exists():
                    HolidayModel.objects.create(title=h['localName'], date=date_str)
            holidays = HolidayModel.objects.filter(date__year=year).order_by('date')
    except Exception:
        pass  # ignore if API fails

    years = list(range(current_year - 5, current_year + 6))

    context = {
        'holidays': holidays,
        'current_year': year,
        'years': years,
    }
    return render(request, 'holidays.html', context)


@login_required
def add_holiday(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date_str = request.POST.get('date')
        
        if title and date_str:
            try:
                date_obj = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
                
                HolidayModel.objects.create(
                    title=title,
                    date=date_obj
                )
                messages.success(request, 'Holiday added successfully!')
                return redirect('holiday_list')
            except ValueError:
                messages.error(request, 'Invalid date format!')
        else:
            messages.error(request, 'Title and Date are required!')
    
    return redirect('holiday_list')

@login_required
def edit_holiday(request, holiday_id):
    holiday = get_object_or_404(HolidayModel, id=holiday_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        date_str = request.POST.get('date')
        
        if title and date_str:
            try:
                # Parse the date string
                date_obj = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
                
                holiday.title = title
                holiday.date = date_obj
                holiday.save()
                messages.success(request, 'Holiday updated successfully!')
                return redirect('holiday_list')
            except ValueError:
                messages.error(request, 'Invalid date format!')
        else:
            messages.error(request, 'Title and Date are required!')
    
    context = {
        'holiday': holiday,
    }
    return render(request, 'edit_holiday.html', context)

@login_required
def delete_holiday(request, holiday_id):
    holiday = get_object_or_404(HolidayModel, id=holiday_id)
    
    if request.method == 'POST':
        holiday.delete()
        messages.success(request, 'Holiday deleted successfully!')
        return redirect('holiday_list')
    
    context = {
        'holiday': holiday,
    }
    return render(request, 'delete_holiday.html', context)

# Notice Management Views
@login_required
def notice_list(request):
    notices = NoticeModel.objects.filter(is_active=True).order_by('-created_at')
    recent_notices = notices[:10]
    return render(request, 'notices/notices.html', {
        'notices': notices,
        'recent_notices': recent_notices
    })


@login_required
def add_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            notice = NoticeModel.objects.create(
                title=title,
                content=content,
                created_by=request.user
            )
            
            # Log activity
            ActivityLogModel.objects.create(
                user=request.user,
                action='create',
                model_name='Notice',
                object_id=notice.id,
                object_repr=notice.title,
                ip_address=ActivityLoggingMiddleware.get_client_ip(request)
            )
            
            messages.success(request, 'Notice created successfully!')
            return redirect('notice_list')
        else:
            messages.error(request, 'Title and content are required!')
    
    return render(request, 'notices/add_notice.html')
# Edit Notice
@login_required
def edit_notice(request, pk):
    notice = get_object_or_404(NoticeModel, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            notice.title = title
            notice.content = content
            notice.save()
            
            # Log activity
            ActivityLogModel.objects.create(
                user=request.user,
                action='update',
                model_name='Notice',
                object_id=notice.id,
                object_repr=notice.title,
                ip_address=ActivityLoggingMiddleware.get_client_ip(request)
            )
            
            messages.success(request, 'Notice updated successfully!')
            return redirect('notice_list')
        else:
            messages.error(request, 'Title and content are required!')
    
    return render(request, 'notices/edit_notice.html', {'notice': notice})


# Delete Notice
@login_required
def delete_notice(request, pk):
    notice = get_object_or_404(NoticeModel, pk=pk)
    
    if request.method == 'POST':
        notice_title = notice.title
        notice.delete()
        
        # Log activity
        ActivityLogModel.objects.create(
            user=request.user,
            action='delete',
            model_name='Notice',
            object_id=pk,
            object_repr=notice_title,
            ip_address=ActivityLoggingMiddleware.get_client_ip(request)
        )
        
        messages.success(request, 'Notice deleted successfully!')
        return redirect('notice_list')
    
    return render(request, 'notices/delete_notice.html', {'notice': notice})

@login_required
def activity_log(request):
    activities = ActivityLogModel.objects.all()[:100]  
    return render(request, 'activities.html', {'activities': activities})

# Signal handlers for login/logout
@login_required
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ActivityLogModel.objects.create(
        user=user,
        action='login',
        model_name='User',
        object_repr=user.username,
        ip_address=ActivityLoggingMiddleware.get_client_ip(request)
    )

@login_required
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ActivityLogModel.objects.create(
        user=user,
        action='logout',
        model_name='User',
        object_repr=user.username,
        ip_address=ActivityLoggingMiddleware.get_client_ip(request)
    )


# List all promotions
@login_required
def promotion_list(request):
    promotions = PromotionModel.objects.select_related(
        "employee", "department", "designation_from", "designation_to"
    )
    for promo in promotions:
        promo.form = PromotionModelForm(instance=promo)

    form = PromotionModelForm()
    return render(request, "promotion_list.html", {
        "promotions": promotions,
        "form": form
    })


# Add new promotion
@login_required
def add_promotion(request):
    if request.method == 'POST':
        form = PromotionModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promotion added successfully.')
        else:
            messages.error(request, 'Please correct the errors below.')
    return redirect('promotion_list')


# Edit existing promotion
@login_required
def edit_promotion(request, promo_id):
    promo = get_object_or_404(PromotionModel, id=promo_id)
    if request.method == 'POST':
        form = PromotionModelForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promotion updated successfully.')
        else:
            messages.error(request, 'Please correct the errors below.')
    return redirect('promotion_list')

@login_required
def delete_promotion(request, promo_id):
    promo = get_object_or_404(PromotionModel, id=promo_id)
    if request.method == 'POST':
        promo.delete()
        messages.success(request, 'Promotion deleted successfully.')
    return redirect('promotion_list')

@login_required
def resignation_list(request):
    resignations = ResignationModel.objects.all().order_by('-resignation_date')
    for res in resignations:
        res.form = ResignationModelForm(instance=res)
    form = ResignationModelForm()
    employees = ProfileModel.objects.all()
    departments = DepartmentModel.objects.all()
    return render(request, 'resignation_list.html', {
        'resignations': resignations,
        'form': form,
        'employees': employees,
        'departments': departments,
    })

@login_required
def approve_resignation(request, pk):
    res = get_object_or_404(ResignationModel, pk=pk)
    if request.method == "POST":
        res.status = "approved"
        res.action_by = request.user.profile
        res.save()
        messages.success(request, f"Resignation of {res.employee.full_name} approved by {res.action_by.full_name}.")
    return redirect('resignation_list')

@login_required
def deny_resignation(request, pk):
    res = get_object_or_404(ResignationModel, pk=pk)
    if request.method == "POST":
        res.status = "denied"
        res.action_by = request.user.profile
        res.save()
        messages.success(request, f"Resignation of {res.employee.full_name} denied by {res.action_by.full_name}.")
    return redirect('resignation_list')

@login_required
def termination_list(request):
    terminations = TerminationModel.objects.all()
    employees = ProfileModel.objects.all()
    departments = DepartmentModel.objects.all()
    context = {
        'terminations': terminations,
        'employees': employees,
        'departments': departments,
    }
    return render(request, 'termination_list.html', context)

@login_required
def add_termination(request):
    if request.method == "POST":
        form = TerminationModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Termination added successfully")
    return redirect('termination_list')

@login_required
def edit_termination(request, pk):
    term = get_object_or_404(TerminationModel, pk=pk)
    if request.method == "POST":
        form = TerminationModelForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            messages.success(request, "Termination updated successfully")
    return redirect('termination_list')

@login_required
def delete_termination(request, pk):
    term = get_object_or_404(TerminationModel, pk=pk)
    if request.method == "POST":
        term.delete()
        messages.success(request, "Termination deleted successfully")
    return redirect('termination_list')


@login_required
def user_list(request):
    users = ProfileModel.objects.all()
    roles = Role.objects.all()
    context = {
        'users': users,
        'roles': roles,
    }
    return render(request, 'user_list.html', context)

@login_required
def profileId(request, pk):
    user = get_object_or_404(ProfileModel, pk=pk)
    return render(request, 'profile.html', {'user': user})

@login_required
def team_list(request):
    teams = TeamModel.objects.select_related("department").all()
    form = TeamForm()

    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Team created successfully")
            return redirect("team_list")

    return render(request, "team_list.html", {"teams": teams, "form": form})


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(TeamModel, id=team_id)
    members = team.members.all()

    if request.user.user_types == 'Admin' and request.method == "POST":
        form = TeamMemberForm(request.POST, team=team)
        if form.is_valid():
            new_member = form.save(commit=False)
            new_member.team = team
            new_member.save()
            messages.success(request, "Member added successfully")
            return redirect('team_detail', team_id=team.id)
    else:
        form = TeamMemberForm(team=team)

    return render(request, 'team_detail.html', {
        'team': team,
        'members': members,
        'form': form
    })


@login_required
def update_member_role(request, member_id):
    member = get_object_or_404(TeamMemberModel, id=member_id)
    if request.method == "POST":
        role = request.POST.get("role")
        if role in dict(TeamMemberModel.ROLE_CHOICES).keys():
            member.role = role
            member.save()
            messages.success(request, "Role updated successfully")
    return redirect("team_detail", team_id=member.team.id)


@login_required
def delete_member(request, member_id):
    member = get_object_or_404(TeamMemberModel, id=member_id)
    team_id = member.team.id
    member.delete()
    messages.success(request, "Member removed successfully")
    return redirect("team_detail", team_id=team_id)