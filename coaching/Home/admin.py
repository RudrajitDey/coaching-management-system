from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User, TeacherAttendance, Routine, StudentAttendance, Department, Holiday


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'subject', 'department', 'fee_pending', 'fee_till_date', 'salary_pending', 'salary_till_date', 'is_staff', 'is_active')
    list_filter = ('role', 'salary_pending', 'salary_till_date', 'fee_pending', 'fee_till_date', 'is_staff', 'is_active')
    search_fields = ('username', 'get_full_name', 'subject')
    list_editable = ('fee_pending', 'fee_till_date', 'salary_pending', 'salary_till_date')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.role == 'teacher':
            # Hide fee fields for teachers
            if 'fee_pending' in form.base_fields:
                form.base_fields.pop('fee_pending')
            if 'fee_till_date' in form.base_fields:
                form.base_fields.pop('fee_till_date')
        elif obj and obj.role == 'student':
            # Hide salary fields for students
            if 'salary_pending' in form.base_fields:
                form.base_fields.pop('salary_pending')
            if 'salary_till_date' in form.base_fields:
                form.base_fields.pop('salary_till_date')
        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ('username', 'email', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            ('Role', {'fields': ('role', 'subject', 'student_class', 'department')}),
            ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ]
        if obj and obj.role == 'teacher':
            fieldsets.append(('Salary', {'fields': ('salary_pending', 'salary_till_date')}))
        elif obj and obj.role == 'student':
            fieldsets.append(('Fees', {'fields': ('fee_pending', 'fee_till_date')}))
        return fieldsets

    def get_add_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ('username', 'email', 'password1', 'password2')}),
            ('Personal info', {'fields': ('first_name', 'last_name')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            ('Role', {'fields': ('role', 'subject', 'student_class', 'department')}),
        ]
        # For add form, we'll use JavaScript to show/hide based on role
        fieldsets.append(('Salary', {'fields': ('salary_pending', 'salary_till_date'), 'classes': ('salary-section',)}))
        fieldsets.append(('Fees', {'fields': ('fee_pending', 'fee_till_date'), 'classes': ('fees-section',)}))
        return fieldsets

    class Media:
        js = ('admin/js/role_fieldset.js',)


class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_till', 'total_present', 'created_at')
    list_filter = ('date_till', 'student__role')
    search_fields = ('student__username', 'student__get_full_name')
    ordering = ('-date_till',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'get_teacher_count', 'get_student_count', 'created_at')
    search_fields = ('name', 'head__username', 'head__get_full_name')
    list_filter = ('created_at',)
    ordering = ('name',)

    def get_teacher_count(self, obj):
        return User.objects.filter(role='teacher', department=obj).count()
    get_teacher_count.short_description = 'Teachers'

    def get_student_count(self, obj):
        return User.objects.filter(role='student', department=obj).count()
    get_student_count.short_description = 'Students'


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    ordering = ('-date',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(TeacherAttendance)
admin.site.register(Routine)
admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Holiday, HolidayAdmin)


