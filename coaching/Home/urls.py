from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home' ),
    
    # path('register/', views.register, name='register' ),

    path('login/', views.login_view, name='login'),

    # Signup
    path('signup/student/', views.student_signup, name="student_signup"),
    path('signup/teacher/', views.teacher_signup, name="teacher_signup"),
    path('signup/admin/', views.admin_signup, name="admin_signup"),

    path('login-redirect/', views.login_redirect, name="login_redirect"),

    # Dashboards
    path('dashboard/admin/', views.admin_dashboard, name="admin_dashboard"),
    path('dashboard/teacher/', views.teacher_dashboard, name="teacher_dashboard"),
    path('dashboard/student/', views.student_dashboard, name="student_dashboard"),
    
    # Teacher Management
    path('teachers/', views.all_teachers, name="all_teachers"),
    path('teacher/<int:teacher_id>/edit/', views.edit_teacher, name="edit_teacher"),
    path('teacher/<int:teacher_id>/delete/', views.delete_teacher, name="delete_teacher"),
    path('teacher-attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('student-attendance/', views.admin_student_attendance, name='student_attendance'),
    path('salary/', views.salary_view, name='salary'),
    path('student-fees/', views.student_fees_view, name='student_fees'),
    path('departments/', views.departments_view, name='departments'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/<int:dept_id>/edit/', views.edit_department, name='edit_department'),
    path('departments/<int:dept_id>/delete/', views.delete_department, name='delete_department'),
    path('holidays/', views.holidays_view, name='holidays'),
    path('routine/', views.routine_view, name='routine'),

    # Student Management
    path('students/', views.all_students, name="all_students"),
    path('students/add/', views.admin_add_student, name="admin_add_student"),
    path("students/edit/<int:student_id>/", views.edit_student, name="edit_student"),
    path("students/delete/<int:student_id>/", views.delete_student, name="delete_student"),


    path('holidays/', views.holiday_list, name='holiday_list'),
    path('holidays/add/', views.add_holiday, name='add_holiday'),
    path('holidays/edit/<int:pk>/', views.edit_holiday, name='edit_holiday'),
    path('holidays/delete/<int:pk>/', views.delete_holiday, name='delete_holiday'),
]