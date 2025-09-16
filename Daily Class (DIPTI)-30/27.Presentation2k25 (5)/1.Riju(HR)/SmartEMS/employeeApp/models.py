from django.db import models
from django.utils import timezone
from datetime import datetime, date
from adminApp.models import ProfileModel, DepartmentModel, DesignationModel, HolidayModel



class TeamModel(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(DepartmentModel, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name


class TeamMemberModel(models.Model):
    ROLE_CHOICES = [
        ('Lead', 'Lead'),
        ('Member', 'Member'),
    ]

    team = models.ForeignKey(TeamModel, on_delete=models.CASCADE, related_name='members')
    member = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='teams')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        unique_together = ('team', 'member') 

    def __str__(self):
        return f"{self.member.full_name} ({self.role}) - {self.team.name}"

# Employee Attendance
class AttendanceModel(models.Model):
    ATTENDANCE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'On Leave'),
    ]

    employee = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.status})"

    @property
    def work_duration(self):
        if self.check_in and self.check_out:
            duration = datetime.combine(date.min, self.check_out) - datetime.combine(date.min, self.check_in)
            return round(duration.total_seconds() / 3600, 2)
        return 0

    @property
    def overtime(self):
        # Overtime = work hours - 8 (only positive)
        return max(self.work_duration - 8, 0)

# Employee Leave Requests
class LeaveRequestModel(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='leave_requests', null=True)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES,null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    reason = models.TextField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending',null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    actioned_by = models.ForeignKey(ProfileModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='leave_actioned_by')
    actioned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-applied_at']
    @property
    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0

    def __str__(self):
        return f"{self.employee.full_name} ({self.start_date} to {self.end_date})"
    
    @property
    def total_days(self):
        """Calculate total number of leave days."""
        return (self.end_date - self.start_date).days + 1

    @property
    def is_active(self):
        """Check if leave is currently ongoing."""
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


# Employee Tasks / Assignments
class TaskModel(models.Model):
    TASK_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='tasks')
    assigned_by = models.ForeignKey(ProfileModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    department = models.ForeignKey(DepartmentModel, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey(DesignationModel, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, choices=TASK_STATUS, default='pending')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

        
    @property
    def remaining_days(self):
        today = timezone.now().date()
        if self.due_date >= today:
            return (self.due_date - today).days
        return -1

    def __str__(self):
        return f"{self.title} - {self.assigned_to.full_name}"


# Employee Notifications (Optional)
class NotificationModel(models.Model):
    employee = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name} - {self.title}"
