from django.shortcuts import render, redirect, get_object_or_404
from adminApp.models import *
from employeeApp.models import *
from employeeApp.forms import *
from adminApp.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import calendar
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from employeeApp.block import block_after_resignation
import os


@login_required
@block_after_resignation
def employee_dashboard(request):
    # Get current user's profile
    profile = ProfileModel.objects.filter(user=request.user).first()
    today = date.today()

    # Assigned tasks for this employee
    assigned_tasks_qs = TaskModel.objects.filter(assigned_to=profile)

    # Prepare tasks with remaining days
    assigned_tasks = []
    for task in assigned_tasks_qs:
        remaining_days = (task.due_date - today).days if task.due_date else None
        assigned_tasks.append({
            'task': task,
            'remaining_days': remaining_days
        })

    # Today's holiday
    today_holiday = HolidayModel.objects.filter(date=today).first()

    # Upcoming holidays (next 5)
    upcoming_holidays = HolidayModel.objects.filter(date__gte=today).order_by('date')[:5]

    # Leave requests for this employee
    leave_requests = LeaveRequestModel.objects.filter(employee=profile)

    # Recent company notices (last 5 active)
    recent_notices = NoticeModel.objects.filter(is_active=True).order_by('-created_at')[:5]

    # Team members in the same position, excluding self
    team_members_qs = ProfileModel.objects.filter(position=profile.position).exclude(id=profile.id)
    team_members = []
    for member in team_members_qs:
        team_members.append({
            'member': member,
            'role': 'Lead' if member.is_team_lead else 'Member'
        })

    # Leave stats
    leave_taken = leave_requests.filter(status='approved').count()
    total_leave = 20  # total leave allowance
    leave_remaining = total_leave - leave_taken

    # Task status counts for charts
    task_status_counts = {
        'pending': assigned_tasks_qs.filter(status='pending').count(),
        'in_progress': assigned_tasks_qs.filter(status='in_progress').count(),
        'completed': assigned_tasks_qs.filter(status='completed').count(),
    }

    # Leave type counts for charts
    leave_type_counts = {
        'annual': leave_requests.filter(leave_type='annual', status='approved').count(),
        'sick': leave_requests.filter(leave_type='sick', status='approved').count(),
        'casual': leave_requests.filter(leave_type='casual', status='approved').count(),
    }

    # Attendance counts (use the related_name 'attendances')
    attendance_counts = {
        'present': profile.attendances.filter(date=today, status='present').count(),
        'absent': profile.attendances.filter(date=today, status='absent').count(),
        'on_leave': leave_requests.filter(status='approved', start_date__lte=today, end_date__gte=today).count()
    }

    context = {
        'profile': profile,
        'today': today,
        'today_holiday': today_holiday,
        'upcoming_holidays': upcoming_holidays,
        'leave_requests': leave_requests,
        'assigned_tasks': assigned_tasks,
        'recent_notices': recent_notices,
        'team_members': team_members,
        'leave_taken': leave_taken,
        'leave_remaining': leave_remaining,
        'task_status_counts': task_status_counts,
        'leave_type_counts': leave_type_counts,
        'attendance_counts': attendance_counts,
    }

    return render(request, 'employee_dashboard.html', context)

@login_required
@block_after_resignation
def leaves_employee(request):
    try:
        profile = ProfileModel.objects.get(user=request.user)
    except ProfileModel.DoesNotExist:
        profile = None

    leaves = LeaveRequestModel.objects.filter(employee=profile).order_by("-applied_at") if profile else LeaveRequestModel.objects.none()

    annual = leaves.filter(leave_type="annual").count()
    sick = leaves.filter(leave_type="sick").count()
    casual = leaves.filter(leave_type="casual").count()
    total_taken = annual + sick + casual
    total_allowed = 20
    remaining = total_allowed - total_taken
    percent_used = int((total_taken / total_allowed) * 100) if total_allowed else 0

    for leave in leaves:
        if leave.start_date and leave.end_date:
            leave.days_count = (leave.end_date - leave.start_date).days + 1
        else:
            leave.days_count = 0

    context = {
        "leaves": leaves,
        "annual": annual,
        "sick": sick,
        "casual": casual,
        "remaining": remaining,
        "total_allowed": total_allowed,
        "percent_used": percent_used,
        "total_taken": total_taken,
    }

    return render(request, "leaves-employee.html", context)



# @csrf_exempt
# def add_leave(request):
#     if request.method != "POST":
#         return JsonResponse({"success": False, "message": "Invalid request method."})

#     try:
#         data = json.loads(request.body)
#         leave_type = data.get("leave_type")
#         start_date = data.get("start_date")
#         end_date = data.get("end_date")
#         reason = data.get("reason")

#         if not all([leave_type, start_date, end_date, reason]):
#             return JsonResponse({"success": False, "message": "All fields are required."})

#         start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#         end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

#         if start_date > end_date:
#             return JsonResponse({"success": False, "message": "Start date cannot be after end date."})

#         try:
#             profile = ProfileModel.objects.get(user=request.user)
#         except ProfileModel.DoesNotExist:
#             return JsonResponse({"success": False, "message": "Profile not found."})

#         leave = LeaveRequestModel.objects.create(
#             employee=profile,
#             leave_type=leave_type,
#             start_date=start_date,
#             end_date=end_date,
#             reason=reason,
#             status='pending'
#         )

#         return JsonResponse({
#             "success": True,
#             "id": leave.id,
#             "leave_type": leave.get_leave_type_display(),
#             "start_date": start_date.strftime("%b %d, %Y"),
#             "end_date": end_date.strftime("%b %d, %Y"),
#             "duration": (end_date - start_date).days + 1,
#             "reason": reason,
#             "status": "Pending"
#         })
#     except Exception as e:
#         return JsonResponse({"success": False, "message": str(e)})


@csrf_exempt
@login_required
@block_after_resignation
def edit_leave(request, pk):
    try:
        profile = ProfileModel.objects.get(user=request.user)
        leave = get_object_or_404(LeaveRequestModel, pk=pk, employee=profile)
    except ProfileModel.DoesNotExist:
        return JsonResponse({"success": False, "message": "Profile not found."})

    if leave.status != "pending":
        return JsonResponse({"success": False, "message": "Only pending leaves can be edited."})

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            form = LeaveRequestForm(data, instance=leave)

            if form.is_valid():
                form.save()
                duration = (leave.end_date - leave.start_date).days + 1 if leave.start_date and leave.end_date else 0
                return JsonResponse({
                    "success": True,
                    "message": "Leave updated successfully.",
                    "leave": {
                        "id": leave.id,
                        "leave_type": leave.get_leave_type_display(),
                        "start_date": leave.start_date.strftime("%b %d, %Y"),
                        "end_date": leave.end_date.strftime("%b %d, %Y"),
                        "duration": duration,
                        "reason": leave.reason,
                        "status": leave.get_status_display(),
                    }
                })
            else:
                return JsonResponse({"success": False, "message": "Form validation failed.", "errors": form.errors})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    # GET request: return leave data
    return JsonResponse({
        "success": True,
        "leave": {
            "id": leave.id,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date.isoformat(),
            "end_date": leave.end_date.isoformat(),
            "reason": leave.reason,
        }
    })

@login_required
@block_after_resignation
def delete_leave(request, pk):
    try:
        profile = ProfileModel.objects.get(user=request.user)
        leave = get_object_or_404(LeaveRequestModel, pk=pk, employee=profile)
        leave.delete()
        messages.success(request, "Leave request cancelled successfully!")
    except ProfileModel.DoesNotExist:
        messages.error(request, "Profile not found.")
    return redirect('leaves_employee')

@login_required
@block_after_resignation
def leave_history(request):
    """
    Display leave history, handle edit and delete actions via POST.
    """
    profile = get_object_or_404(ProfileModel, user=request.user)
    leaves_list = LeaveRequestModel.objects.filter(employee=profile).order_by('-start_date')

    # Handle POST requests for edit or delete
    if request.method == 'POST':
        # Edit Leave
        if 'edit_leave_id' in request.POST:
            leave_id = request.POST.get('edit_leave_id')
            leave = get_object_or_404(LeaveRequestModel, pk=leave_id, employee=profile)
            form = LeaveRequestForm(request.POST, instance=leave)
            if form.is_valid():
                form.save()
                messages.success(request, "Leave updated successfully.")
            else:
                messages.error(request, "Failed to update leave. Please check your inputs.")
            return redirect('leave_history')

        # Delete Leave
        elif 'delete_leave_id' in request.POST:
            leave_id = request.POST.get('delete_leave_id')
            leave = get_object_or_404(LeaveRequestModel, pk=leave_id, employee=profile)
            leave.delete()
            messages.success(request, "Leave deleted successfully.")
            return redirect('leave_history')

    # Pagination
    paginator = Paginator(leaves_list, 10)  # Show 10 leaves per page
    page_number = request.GET.get('page')
    leaves = paginator.get_page(page_number)

    context = {
        'leaves': leaves,
    }
    return render(request, 'leaves_history.html', context)

@login_required
@block_after_resignation
def add_leave(request):
    profile = get_object_or_404(ProfileModel, user=request.user)
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = profile
            leave.save()
            messages.success(request, "Leave request submitted successfully.")
            return redirect('leave_history')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = LeaveRequestForm()

    return render(request, 'add_leave.html', {'form': form})
# UPDATE
@login_required
@block_after_resignation
def edit_leave(request, pk):
    leave = get_object_or_404(LeaveRequestModel, pk=pk, employee__user=request.user)
    if request.method == "POST":
        form = LeaveRequestForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave request updated successfully.")
            return redirect('employee_dashboard')
    else:
        form = LeaveRequestForm(instance=leave)
    return render(request, "edit_leave.html", {"form": form})

# DELETE
@login_required
@block_after_resignation
def delete_leave(request, pk):
    leave = get_object_or_404(LeaveRequestModel, pk=pk, employee__user=request.user)
    if request.method == "POST":
        leave.delete()
        messages.success(request, "Leave request deleted successfully.")
        return redirect('employee_dashboard')
    return render(request, "delete_leave.html", {"leave": leave})

# READ (optional: single leave details)
@login_required
@block_after_resignation
def leave_detail(request, pk):
    leave = get_object_or_404(LeaveRequestModel, pk=pk, employee__user=request.user)
    return render(request, "leave_detail.html", {"leave": leave})

@login_required
@block_after_resignation
def timedelta_to_hours(td):
    if isinstance(td, (int, float)):  # already in hours
        return round(td, 2)
    if td:  # timedelta case
        return round(td.total_seconds() / 3600, 2)
    return 0

@login_required
@block_after_resignation
def attendance_dashboard(request):
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

    # Monthly Summary
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
    return render(request, 'attendance_dashboard.html', context)



@login_required
@block_after_resignation
def punch_out(request, pk):
    att = get_object_or_404(AttendanceModel, pk=pk, employee__user=request.user)
    if not att.check_out:
        att.check_out = now()
        # calculate work_duration
        if att.check_in:
            duration = (att.check_out - att.check_in).seconds / 3600
            att.work_duration = round(duration, 2)
        att.save()
    return redirect('attendance_dashboard')

@login_required
@block_after_resignation
def attendance_list(request):
    attendances = AttendanceModel.objects.select_related('employee').all()
    return render(request, 'attendance_list.html', {'attendances': attendances})

@login_required
@block_after_resignation
def add_attendance(request):
    user = request.user

    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)

            # Auto-assign employee for Employee users
            if user.user_types == 'Employee':
                try:
                    profile = ProfileModel.objects.get(user=user)
                    attendance.employee = profile
                except ProfileModel.DoesNotExist:
                    messages.error(request, "Your profile is missing. Please contact admin.")
                    return redirect('attendance_list')

            attendance.save()
            messages.success(request, "Attendance added successfully.")
            return redirect('attendance_list')
    else:
        # Pre-populate today's date
        form = AttendanceForm(initial={"date": now().date()})

        # Safely remove employee field for Employee users
        if user.user_types == 'Employee':
            form.fields.pop('employee', None)  # <-- safe pop

    context = {
        'form': form,
        'title': 'Add Attendance',
    }
    return render(request, 'add_attendance.html', context)

@login_required
@block_after_resignation
def edit_attendance(request, pk):
    attendance = get_object_or_404(AttendanceModel, pk=pk)
    user = request.user

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            attendance_obj = form.save(commit=False)

            # Ensure Employee users cannot change the employee field
            if user.user_types == 'Employee':
                profile = ProfileModel.objects.get(user=user)
                attendance_obj.employee = profile

            attendance_obj.save()
            messages.success(request, 'Attendance updated successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)

        # Hide employee field for Employee users safely
        if user.user_types == 'Employee':
            form.fields.pop('employee', None)

    return render(request, 'attendance_form.html', {'form': form, 'title': 'Edit Attendance'})

@login_required
@block_after_resignation
def delete_attendance(request, pk):
    attendance = get_object_or_404(AttendanceModel, pk=pk)
    attendance.delete()
    messages.success(request, 'Attendance deleted successfully.')
    return redirect('attendance_list')

@login_required
@block_after_resignation
def employee_activities(request):
    activities_qs = ActivityLogModel.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(activities_qs, 10)
    page_number = request.GET.get('page')
    activities = paginator.get_page(page_number)

    context = {
        'activities': activities
    }
    return render(request, 'activities.html', context)


#--------------------------------------Task-----------------------------------------
@login_required
@block_after_resignation
def task_list(request):
    # All tasks
    tasks = TaskModel.objects.all()

    # Check if the user is a team lead
    is_team_lead = request.user.profile.is_team_lead

    # Define statuses with colors for Kanban columns
    statuses = [
        ('pending', 'danger'),
        ('in_progress', 'warning'),
        ('completed', 'success'),
    ]

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'is_team_lead': is_team_lead,
        'statuses': statuses, 
    })

@login_required
@block_after_resignation
def add_task(request):
    profile = get_object_or_404(ProfileModel, user=request.user)
    is_team_leader = TeamMemberModel.objects.filter(member=profile, role='Lead').exists()
    
    if not is_team_leader:
        messages.error(request, "Only team leaders can assign tasks.")
        return redirect('task_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = profile
            task.save()
            messages.success(request, "Task assigned successfully!")
            return redirect('task_list')
    else:
        form = TaskForm(user=request.user)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Add Task'})

@login_required
@block_after_resignation
def edit_task(request, pk):
    task = get_object_or_404(TaskModel, pk=pk)
    profile = get_object_or_404(ProfileModel, user=request.user)

    # Only the assigner can edit
    if task.assigned_by != profile:
        messages.error(request, "You do not have permission to edit this task.")
        return redirect('task_list')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})

@login_required
@block_after_resignation
def delete_task(request, pk):
    task = get_object_or_404(TaskModel, pk=pk)
    profile = get_object_or_404(ProfileModel, user=request.user)

    if task.assigned_by != profile:
        messages.error(request, "You do not have permission to delete this task.")
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
@block_after_resignation
def task_detail(request, pk):
    task = get_object_or_404(TaskModel, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
@block_after_resignation
def update_task_status(request, pk):
    task = get_object_or_404(TaskModel, pk=pk)

    # Only the assigned employee can change the status
    if task.assigned_to != request.user.profile:
        messages.error(request, "You cannot update this task.")
        return redirect('task_list')

    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task status updated successfully.")
            return redirect('task_list')
    else:
        form = TaskStatusForm(instance=task)

    return render(request, 'tasks/task_update_status.html', {'form': form, 'task': task})

@login_required
@block_after_resignation
def task_board(request):
    tasks = TaskModel.objects.all()
    is_team_lead = request.user.profile.is_team_lead

    # Define task statuses with colors
    statuses = [
        ('pending', 'danger'),
        ('in_progress', 'warning'),
        ('completed', 'success'),
    ]

    return render(request, 'tasks/task_board.html', {
        'tasks': tasks,
        'is_team_lead': is_team_lead,
        'statuses': statuses,
    })


@login_required
@block_after_resignation
def resignation(request):
    resignations = ResignationModel.objects.filter(employee=request.user.profile).order_by('-resignation_date')
    
    for res in resignations:
        res.form = ResignationModelForm(instance=res)
    
    form = ResignationModelForm() 
    return render(request, 'resignation.html', {
        'resignations': resignations,
        'form': form,
    })

@login_required
@block_after_resignation
def add_resignation(request):
    if request.method == "POST":
        form = ResignationModelForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.employee = request.user.profile
            if request.user.profile.position:
                res.department = request.user.profile.position.department
            else:
                res.department = None
            res.notice_date = timezone.now().date()
            res.save()
            messages.success(request, "Resignation submitted successfully.")
        else:
            messages.error(request, "Error submitting resignation.")
    return redirect('resignation')

@login_required
@block_after_resignation
def edit_resignation(request, pk):
    res = get_object_or_404(ResignationModel, pk=pk)
    if request.method == "POST":
        form = ResignationModelForm(request.POST, instance=res)
        if form.is_valid():
            updated_res = form.save(commit=False)
            updated_res.department = res.department
            updated_res.notice_date = res.notice_date
            updated_res.save()
            messages.success(request, "Resignation updated successfully.")
        else:
            messages.error(request, "Error updating resignation.")
    return redirect('resignation')


@login_required
@block_after_resignation
def delete_resignation(request, pk):
    res = get_object_or_404(ResignationModel, pk=pk)
    if request.method == "POST":
        res.delete()
        messages.success(request, "Resignation deleted successfully.")
    return redirect('resignation')


@login_required
def employee_profile(request):
    profile = request.user.profile
    resignation = ResignationModel.objects.filter(employee=profile, status='approved').first()
    if not resignation:
        return HttpResponseForbidden("Profile accessible only after resignation approval.")

    # Pass profile and certificate URL
    return render(request, 'employee_profile.html', {
        'profile': profile,
        'certificate_url': f'/employee_certificate/{profile.id}/',
    })


@login_required
def employee_certificate(request, profile_id):
    profile = get_object_or_404(ProfileModel, id=profile_id)

    if profile.user != request.user:
        return HttpResponseForbidden("You are not allowed to access this certificate.")

    resignation = ResignationModel.objects.filter(employee=profile, status='approved').first()

    return render(request, 'experience_certificate.html', {
        'profile': profile,
        'resignation': resignation,
    })