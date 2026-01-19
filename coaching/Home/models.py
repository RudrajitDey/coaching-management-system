from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError



class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    subject = models.CharField(max_length=100, blank=True, null=True)
    student_class = models.CharField(max_length=50, blank=True, null=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    salary_pending = models.BooleanField(default=True)
    salary_till_date = models.DateField(null=True, blank=True)
    fee_pending = models.BooleanField(default=True)
    fee_till_date = models.DateField(null=True, blank=True)

    objects = CustomUserManager()


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records', 
     limit_choices_to={'role': 'teacher'})
    date_till = models.DateField(null=True, blank=True)
    total_present = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('teacher', 'date_till')
        ordering = ['-date_till']

    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.date_till}"


class StudentAttendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_attendance_records',
     limit_choices_to={'role': 'student'})
    date_till = models.DateField(null=True, blank=True)
    total_present = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'date_till')
        ordering = ['-date_till']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.date_till}"
    

class StudentFees(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fee_records',
     limit_choices_to={'role': 'student'})
    fee_pending = models.BooleanField(default=True)
    fee_till_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'fee_till_date')
        ordering = ['-fee_till_date']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.fee_till_date}"
    

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
     related_name='department_head', limit_choices_to={'role': 'teacher'})
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} - {self.date}"
    

    from django.db import models
from django.core.exceptions import ValidationError


class Routine(models.Model):
    DAYS = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    ]

    class_name = models.CharField(max_length=50)
    batch = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    days = models.CharField(max_length=100, default='MON', help_text="Enter days separated by commas, e.g., MON,TUE,WED")
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['class_name', 'batch', 'start_time']
        unique_together = (
            'class_name',
            'batch',
            'start_time',
            'end_time'
        )

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")

    def __str__(self):
        return f"{self.class_name} | {self.batch} | {self.days} | {self.subject}"



from django.db import models

class Holiday(models.Model):
    date = models.DateField()
    day = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
