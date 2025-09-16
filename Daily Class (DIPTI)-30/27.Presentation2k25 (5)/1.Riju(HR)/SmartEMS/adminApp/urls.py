from django.urls import path
from adminApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('my-profile/', profile_view, name='my_profile'),
    path('update-profile/', update_profile, name='update_profile'),
    path('profile/<int:user_id>/', view_profile, name='view_profile'),
    path('update-team-member-role/<int:pk>/', update_team_member_role, name='update_team_member_role'),

    path('add-admin/', add_admin, name='add_admin'),


    path('add-department/', addDepartment, name='addDepartment'),
    path('departments/', departments, name='departments'),
    path('departments/edit/<int:dept_id>/', editDepartment, name='editDepartment'),
    path('departments/delete/<int:dept_id>/', deleteDepartment, name='deleteDepartment'),

    path('designations/', designation_list, name='designation_list'),
    path('designations/add/', add_designation, name='add_designation'),
    path('designations/edit/<int:desig_id>/', edit_designation, name='edit_designation'),
    path('designations/delete/<int:desig_id>/', delete_designation, name='delete_designation'),

    path('add-employee/', add_employee, name='add_employee'),
    path('employeeList/', employeeList, name='employeeList'),
    path('employeeListView/', employeeListView, name='employeeListView'),
    path('employee/edit/<int:pk>/', edit_profile, name='update_profile'),
    path('employee/delete/<int:pk>/', delete_employee, name='delete_employee'),

    path('add-leave/', addLeave, name='addLeave'),
    path('leavesList/', leavesList, name='leavesList'),
    path('leave-requests/', leave_requests_admin_view, name='admin_leave_requests'),

    path('attendance-dashboard/', attendanceDashboard, name='attendanceDashboard'),
    path('attendance/', attendance, name='attendance'),

    path('holidays/', holiday_list, name='holiday_list'),
    path('holidays/add/', add_holiday, name='add_holiday'),
    path('holidays/edit/<int:holiday_id>/', edit_holiday, name='edit_holiday'),
    path('holidays/delete/<int:holiday_id>/', delete_holiday, name='delete_holiday'),

    path('notices/', notice_list, name='notice_list'),
    path('notices/add/', add_notice, name='add_notice'),
    path('notices/<int:pk>/edit/', edit_notice, name='edit_notice'),
    path('notices/<int:pk>/delete/', delete_notice, name='delete_notice'),
    path('activity-log/', activity_log, name='activity_log'),

    path('promotion-list/', promotion_list, name='promotion_list'),
    path('add-promotion/', add_promotion, name='add_promotion'),
    path('edit-promotion/<int:promo_id>/', edit_promotion, name='edit_promotion'),
    path('delete-promotion/<int:promo_id>/', delete_promotion, name='delete_promotion'),

    path('resignation-list/', resignation_list, name='resignation_list'),
    path('approve_resignation/<int:pk>/', approve_resignation, name='approve_resignation'),
    path('deny_resignation/<int:pk>/', deny_resignation, name='deny_resignation'),

    path('termination-list/', termination_list, name='termination_list'),
    path('add-termination/', add_termination, name='add_termination'),
    path('edit-termination/<int:pk>/', edit_termination, name='edit_termination'),
    path('delete-termination/<int:pk>/', delete_termination, name='delete_termination'),

    path('user_list/', user_list, name='user_list'),
    path('profile/<int:pk>/', profileId, name='profile'),

    path("teams/", team_list, name="team_list"),
    path("teams/<int:team_id>/", team_detail, name="team_detail"),
    path("update-member/<int:member_id>/", update_member_role, name="update_member_role"),
    path("delete-member/<int:member_id>/", delete_member, name="delete_member"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)