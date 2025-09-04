from django.contrib import admin
from django.urls import path
from PreSchool.views import *
from PreSchool.teacherviews import *
from PreSchool.studentviews import *
from PreSchool.departmentviews import *
from PreSchool.subjectviews import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signupPage/',signupPage,name="signupPage"),
    path('',signinPage,name="signinPage"),
    path('logoutPage/',logoutPage,name="logoutPage"),
    
    #--------Teacher Route--------------
    path('teacherDashboard/',teacherDashboard,name="teacherDashboard"),
    path('addTeacher/',addTeacher,name="addTeacher"),
    path('editTeacher/',editTeacher,name="editTeacher"),
    path('teacherDetails/',teacherDetails,name="teacherDetails"),
    path('teacherList/',teacherList,name="teacherList"),
    
    #--------Admin Route--------------
    path('adminDashboard/',adminDashboard,name="adminDashboard"),
    
    #--------Students Route--------------
    path('studentDashboard/',studentDashboard,name="studentDashboard"),
    path('addStudent/',addStudent,name="addStudent"),
    path('editStudent/<str:myid>',editStudent,name="editStudent"),
    path('studentList/',studentList,name="studentList"),
    path('studentDetails/<str:myid>',studentDetails,name="studentDetails"),
    path('deleteStudent/<str:myid>',deleteStudent,name="deleteStudent"),
    
    #--------Department Route--------------
    path('addDepartment/',addDepartment,name="addDepartment"),
    path('editDepartment/<str:myid>',editDepartment,name="editDepartment"),
    path('viewDepartment/<str:myid>',viewDepartment,name="viewDepartment"),
    path('departmentList/',departmentList,name="departmentList"),
    path('deleteDepartment/<str:myid>',deleteDepartment,name="deleteDepartment"),
    
    #--------Subject Route--------------
    path('addSubject/',addSubject,name="addSubject"),
    path('editSubject/',editSubject,name="editSubject"),
    path('subjectList/',subjectList,name="subjectList"),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
