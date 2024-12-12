from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Student,Topic, Question, StudentResponse,StudentTopicPoints,StudentOtherData
from .forms import StudentCreationForm, StudentChangeForm

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'text', 'options', 'points')

@admin.register(StudentResponse)
class StudentResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'question', 'answer', 'points')

@admin.register(StudentTopicPoints)
class StudentTopicPointsAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'total_points')
    search_fields = ('student__email', 'topic__name')
    list_filter = ('student', 'topic')
@admin.register(StudentOtherData)
class StudentOtherDataAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_of_birth', 'math_marks', 'science_marks', 'social_science_marks', 'parental_influence', 'area_choice', 'parent_education')

class UserAdmin(BaseUserAdmin):
    model = Student
    add_form = StudentCreationForm
    form = StudentChangeForm
    list_display = ('email', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'mobile_no')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile_no', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Student, UserAdmin)
