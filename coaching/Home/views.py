from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Routine
from .models import Holiday
# Create your views here.

def index(request):
    context = {
        "total_courses": 6,
        "total_projects": 40,
        "test_attended": 30,
        "test_passed": 15,
    }
    return render(request, "index.html", context)

# def login(request):
#     return render(request, "login.html")

# def register(request):
#     return render(request, "register.html") 


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import User, TeacherAttendance, StudentAttendance, Department, Holiday
from .forms import StudentSignupForm, TeacherSignupForm, DepartmentForm


# -------------------------
# STUDENT SIGNUP (OPEN)
# -------------------------
def student_signup(request):
    form = StudentSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "student"
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('student_dashboard')
    return render(request, "signup/student_signup.html", {"form": form})


# -------------------------
# ADMIN ADD STUDENT (ONLY ADMIN)
# -------------------------
@login_required
def admin_add_student(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admin can add students.")
    
    form = StudentSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "student"
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('admin_dashboard')
    return render(request, "admin/add_student.html", {"form": form})


# -------------------------
# TEACHER SIGNUP (ONLY ADMIN)
# -------------------------
def teacher_signup(request):
    if not request.user.is_authenticated or request.user.role != "admin":
        return HttpResponseForbidden("Only admin can create teacher accounts.")

    form = TeacherSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "teacher"
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('admin_dashboard')
    return render(request, "signup/teacher_signup.html", {"form": form})


# -------------------------
# ADMIN SIGNUP (ONLY IF NO ADMIN EXISTS)
# -------------------------
def admin_signup(request):
    if User.objects.filter(role="admin").exists():
        return HttpResponseForbidden("Admin already exists.")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            password=password,
            role='admin'
        )
        login(request, user)
        return redirect('admin_dashboard')

    return render(request, "signup/admin_signup.html")


# -------------------------
# LOGIN REDIRECT
# -------------------------
@login_required
def login_redirect(request):
    if request.user.role == "admin":
        return redirect('admin_dashboard')
    elif request.user.role == "teacher":
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')


# -------------------------
# DASHBOARDS
# -------------------------
@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Not allowed.")
    return render(request, "dashboard/admin.html")


@login_required
def teacher_dashboard(request):
    if request.user.role != "teacher":
        return HttpResponseForbidden("Not allowed.")
    return render(request, "dashboard/teacher.html")


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return HttpResponseForbidden("Not allowed.")
    return render(request, "dashboard/student.html")


# -------------------------
# TEACHER MANAGEMENT
# -------------------------
@login_required
def all_teachers(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Not allowed.")
    
    teachers = User.objects.filter(role="teacher")
    
    # Filter by subject if provided
    subject_filter = request.GET.get('subject', '')
    if subject_filter:
        teachers = teachers.filter(subject=subject_filter)
    
    # Get all unique subjects for filter dropdown
    all_subjects = User.objects.filter(role="teacher").values_list('subject', flat=True).distinct().order_by('subject')
    
    return render(request, "admin/all_teacher.html", {
        "teachers": teachers,
        "all_subjects": all_subjects,
        "selected_subject": subject_filter
    })


@login_required
def edit_teacher(request, teacher_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("Not allowed.")
    
    teacher = User.objects.get(id=teacher_id, role="teacher")
    
    if request.method == "POST":
        teacher.username = request.POST.get("username")
        teacher.subject = request.POST.get("subject")
        teacher.save()
        return redirect("all_teachers")
    
    return render(request, "admin/edit_teacher.html", {"teacher": teacher})


@login_required
def delete_teacher(request, teacher_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("Not allowed.")
    
    teacher = User.objects.get(id=teacher_id, role="teacher")
    teacher.delete()
    return redirect("all_teachers")


@login_required
def all_students(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Not allowed.")

    students = User.objects.filter(role="student")

    selected_class = request.GET.get('student_class')
    if selected_class:
        students = students.filter(student_class=selected_class)

    all_classes = (
        User.objects
        .filter(role="student")
        .values_list('student_class', flat=True)
        .distinct()
        .order_by('student_class')
    )

    return render(request, "admin/all_student.html", {
        "students": students,
        "all_classes": all_classes,
        "selected_class": selected_class,
    })


@login_required
def edit_student(request, student_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("Not allowed.")
    
    student = User.objects.get(id=student_id, role="student")
    
    if request.method == "POST":
        student.username = request.POST.get("username")
        student.student_class = request.POST.get("student_class")
        student.save()
        return redirect("all_students")
    
    return render(request, "admin/edit_student.html", {"student": student})


@login_required
def delete_student(request, student_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("Not allowed.")
    
    student = User.objects.get(id=student_id, role="student")
    student.delete()
    return redirect("all_students")


# -------------------------
# SALARY MANAGEMENT
# -------------------------
@login_required
def salary_view(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admin can view salary status.")
    
    teachers = User.objects.filter(role="teacher")
    return render(request, "admin/salary.html", {"teachers": teachers})


@login_required
def student_fees_view(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admin can view fee status.")
    
    students = User.objects.filter(role="student")
    return render(request, "admin/student_fees.html", {"students": students})


@login_required
def departments_view(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admin can view departments.")
    
    departments = Department.objects.prefetch_related('head').all()
    # Add teacher and student counts
    for dept in departments:
        dept.teacher_count = User.objects.filter(role='teacher', department=dept).count()
        dept.student_count = User.objects.filter(role='student', department=dept).count()
    
    return render(request, "admin/departments.html", {"departments": departments})


@login_required
def add_department(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admin can add departments.")
    
    form = DepartmentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("departments")
    
    return render(request, "admin/add_department.html", {"form": form})


@login_required
def edit_department(request, dept_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admin can edit departments.")
    
    department = get_object_or_404(Department, id=dept_id)
    form = DepartmentForm(request.POST or None, instance=department)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("departments")
    
    return render(request, "admin/edit_department.html", {"form": form, "department": department})


@login_required
def delete_department(request, dept_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admin can delete departments.")
    
    department = get_object_or_404(Department, id=dept_id)
    department.delete()
    return redirect("departments")


@login_required
def holidays_view(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admin can view holidays.")
    
    holidays = Holiday.objects.all().order_by('-date')
    return render(request, "admin/holiday_list.html", {"holidays": holidays})


from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("login_redirect")   # this uses your role redirect function
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "registration/login.html")

#Teacher Attendance View
def teacher_attendance(request):
    from .models import TeacherAttendance
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance_id = data.get('id')
            date_till = data.get('date_till')
            total_present = data.get('total_present')
            
            if attendance_id:
                attendance = TeacherAttendance.objects.get(id=attendance_id)
                attendance.date_till = date_till
                attendance.total_present = int(total_present)
                attendance.save()
                return JsonResponse({'status': 'success', 'message': 'Attendance updated'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # Get all teachers
    teachers = User.objects.filter(role='teacher')
    
    # Get or create attendance records for teachers
    attendance_data = []
    for idx, teacher in enumerate(teachers, 1):
        latest_attendance = TeacherAttendance.objects.filter(teacher=teacher).first()
        if latest_attendance:
            attendance_data.append({
                'id': latest_attendance.id,
                'sl': idx,
                'name': teacher.get_full_name() or teacher.username,
                'subject': teacher.subject or 'N/A',
                'date_till': latest_attendance.date_till.isoformat() if latest_attendance.date_till else '',
                'total_present': latest_attendance.total_present
            })
        else:
            # Create default attendance record
            new_attendance = TeacherAttendance.objects.create(teacher=teacher)
            attendance_data.append({
                'id': new_attendance.id,
                'sl': idx,
                'name': teacher.get_full_name() or teacher.username,
                'subject': teacher.subject or 'N/A',
                'date_till': '',
                'total_present': 0
            })
    
    context = {
        'attendance_data': attendance_data
    }
    return render(request, 'teacher_manage/attendance.html', context)


# Student Attendance View
@login_required
def admin_student_attendance(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admin can view student attendance.")
    
    from .models import StudentAttendance
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance_id = data.get('id')
            date_till = data.get('date_till')
            total_present = data.get('total_present')
            
            if attendance_id:
                attendance = StudentAttendance.objects.get(id=attendance_id)
                attendance.date_till = date_till
                attendance.total_present = int(total_present)
                attendance.save()
                return JsonResponse({'status': 'success', 'message': 'Attendance updated'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # Get all students
    students = User.objects.filter(role='student')
    
    # Get or create attendance records for students
    attendance_data = []
    for idx, student in enumerate(students, 1):
        latest_attendance = StudentAttendance.objects.filter(student=student).first()
        if latest_attendance:
            attendance_data.append({
                'id': latest_attendance.id,
                'sl': idx,
                'name': student.get_full_name() or student.username,
                'class_name': student.student_class or 'Not Assigned',
                'date_till': latest_attendance.date_till.isoformat() if latest_attendance.date_till else '',
                'total_present': latest_attendance.total_present
            })
        else:
            # Create default attendance record
            new_attendance = StudentAttendance.objects.create(student=student)
            attendance_data.append({
                'id': new_attendance.id,
                'sl': idx,
                'name': student.get_full_name() or student.username,
                'class_name': student.student_class or 'Not Assigned',
                'date_till': '',
                'total_present': 0
            })
    
    context = {
        'attendance_data': attendance_data
    }
    return render(request, 'admin/student_attendance_new.html', context)


def routine_view(request):
    selected_day = request.GET.get('day', '')
    routines = Routine.objects.all()
    if selected_day:
        routines = routines.filter(days__contains=selected_day)
    routines = routines.order_by('class_name', 'batch', 'start_time')
    days = [choice[0] for choice in Routine.DAYS]
    return render(request, 'teacher_manage/routine.html', {
        'routines': routines,
        'selected_day': selected_day,
        'days': days
    })


#Holiday View

def holiday_list(request):
    holidays = Holiday.objects.all().order_by('date')
    return render(request, 'admin/holiday_list.html', {'holidays': holidays})

def add_holiday(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        day = request.POST.get('day')
        name = request.POST.get('name')

        Holiday.objects.create(
            date=date,
            day=day,
            name=name
        )
        return redirect('holiday_list')

    return render(request, 'admin/holiday_add.html')

def edit_holiday(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)

    if request.method == 'POST':
        holiday.date = request.POST.get('date')
        holiday.day = request.POST.get('day')
        holiday.name = request.POST.get('name')
        holiday.save()
        return redirect('holiday_list')

    return render(request, 'admin/holiday_edit.html', {'holiday': holiday})

def delete_holiday(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == 'POST':
        holiday.delete()
        return redirect('holiday_list')
    return render(request, 'admin/holiday_delete.html', {'holiday': holiday})
    return render(request, 'holiday_delete.html', {'holiday': holiday})