# EmployeeApp/urls.py
from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    # Dashboard URLs
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    
    # User Management URLs
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    # Job Post URLs
    path('job-posts/', views.JobPostListView.as_view(), name='jobpost_list'),
    path('job-posts/<int:pk>/', views.JobPostDetailView.as_view(), name='jobpost_detail'),
    path('job-posts/create/', views.JobPostCreateView.as_view(), name='jobpost_create'),
    path('job-posts/<int:pk>/update/', views.JobPostUpdateView.as_view(), name='jobpost_update'),
    path('job-posts/<int:pk>/delete/', views.JobPostDeleteView.as_view(), name='jobpost_delete'),
    
    # Application URLs
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/update/', views.ApplicationUpdateView.as_view(), name='application_update'),
    
    # Interview URLs
    path('interviews/', views.InterviewListView.as_view(), name='interview_list'),
    path('interviews/<int:pk>/', views.InterviewDetailView.as_view(), name='interview_detail'),
    path('interviews/create/', views.InterviewCreateView.as_view(), name='interview_create'),
    path('interviews/<int:pk>/update/', views.InterviewUpdateView.as_view(), name='interview_update'),
    
    # Course URLs
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
    # Course Teacher URLs
    path('course-teachers/', views.CourseTeacherListView.as_view(), name='courseteacher_list'),
    path('course-teachers/create/', views.CourseTeacherCreateView.as_view(), name='courseteacher_create'),
    path('course-teachers/<int:pk>/update/', views.CourseTeacherUpdateView.as_view(), name='courseteacher_update'),
    path('course-teachers/<int:pk>/delete/', views.CourseTeacherDeleteView.as_view(), name='courseteacher_delete'),
    
    # Assignment URLs
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignments/create/', views.AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:pk>/update/', views.AssignmentUpdateView.as_view(), name='assignment_update'),
    path('assignments/<int:pk>/delete/', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
    
    # Lesson Plan URLs
    path('lesson-plans/', views.LessonPlanListView.as_view(), name='lessonplan_list'),
    path('lesson-plans/<int:pk>/', views.LessonPlanDetailView.as_view(), name='lessonplan_detail'),
    path('lesson-plans/create/', views.LessonPlanCreateView.as_view(), name='lessonplan_create'),
    path('lesson-plans/<int:pk>/update/', views.LessonPlanUpdateView.as_view(), name='lessonplan_update'),
    path('lesson-plans/<int:pk>/delete/', views.LessonPlanDeleteView.as_view(), name='lessonplan_delete'),
    
    # Class Routine URLs
    path('class-routines/', views.ClassRoutineListView.as_view(), name='classroutine_list'),
    path('class-routines/<int:pk>/', views.ClassRoutineDetailView.as_view(), name='classroutine_detail'),
    path('class-routines/create/', views.ClassRoutineCreateView.as_view(), name='classroutine_create'),
    path('class-routines/<int:pk>/update/', views.ClassRoutineUpdateView.as_view(), name='classroutine_update'),
    path('class-routines/<int:pk>/delete/', views.ClassRoutineDeleteView.as_view(), name='classroutine_delete'),
    
    # Attendance URLs
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance_detail'),
    path('attendance/create/', views.AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/<int:pk>/update/', views.AttendanceUpdateView.as_view(), name='attendance_update'),
    
    # Export Data URLs
    path('export/employee-data/', views.export_employee_data, name='export_employee_data'),
    path('export/job-data/', views.export_job_data, name='export_job_data'),
    path('export/application-data/', views.export_application_data, name='export_application_data'),
    path('export/course-data/', views.export_course_data, name='export_course_data'),
    path('export/assignment-data/', views.export_assignment_data, name='export_assignment_data'),
    path('export/lessonplan-data/', views.export_lessonplan_data, name='export_lessonplan_data'),
    path('export/attendance-data/', views.export_attendance_data, name='export_attendance_data'),
    
    # Chart Data URLs
    path('chart-data/hr/', views.hr_chart_data, name='hr_chart_data'),
    path('chart-data/faculty/', views.faculty_chart_data, name='faculty_chart_data'),
    path('chart-data/teacher/', views.teacher_chart_data, name='teacher_chart_data'),

    # Enrollment URLs
    path('pending-enrollments-table/', views.pending_enrollments_table, name='pending_enrollments_table'),
    path('enrollment-action/<int:enrollment_id>/<str:action>/', views.enrollment_action, name='enrollment_action'),
]