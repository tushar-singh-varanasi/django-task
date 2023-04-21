from django.urls import path
from .import views

urlpatterns = [
   
    path('registration/',views.TeacherResgistratipn.as_view(),name='resgistration'),
    path('login/',views.UserLogin.as_view(),name='login'),
    path('teacher/',views.StudentResgistratipn.as_view(),name='techer'),
    path('student/',views.StudentProfile.as_view(),name='student'),
    path('admin-teacher/',views.AdminAddTeacher.as_view(),name='admin_user'),
    path("admin-student/",views.AdminAddStudent.as_view(), name="admin_student"),
    path('changepassword/',views.UserChangePassword.as_view(),name='changepassword'),
    path('send-password-reset-link/',views.SendPasswordResetEmail.as_view(),name='send-password-link'),
    path('reset-password/<uid>/<token>/',views.UserPasswordReset.as_view(),name='reset-password')
]
