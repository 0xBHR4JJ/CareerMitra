from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Student

class StudentCreationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ('email', 'name', 'mobile_no')

class StudentChangeForm(UserChangeForm):
    class Meta:
        model = Student
        fields = ('email', 'name', 'mobile_no', 'is_active', 'is_staff')
