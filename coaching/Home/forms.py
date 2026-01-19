from django import forms
from .models import User, Department

class StudentSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    student_class = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'student_class']


class TeacherSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'subject']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'head', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }