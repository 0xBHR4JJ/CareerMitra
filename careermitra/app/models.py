from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Student(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Django handles hashing the password

    # Additional fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_no']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # All users have access to all permissions
        return True

    def has_module_perms(self, app_label):
        # All users have access to all modules
        return True
    
class Topic(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    options = models.JSONField()  # Store options as JSON
    points = models.JSONField()   # Store points for each option as JSON

    def __str__(self):
        return self.text

class StudentResponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.student.email} - {self.question.text}"
class StudentTopicPoints(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    total_points = models.IntegerField()

    class Meta:
        unique_together = ('student', 'topic')

    def __str__(self):
        return f"{self.student.email} - {self.topic.name} - {self.total_points}"

# Signal to update StudentTopicPoints when a StudentResponse is saved
@receiver(post_save, sender=StudentResponse)
def update_student_topic_points(sender, instance, **kwargs):
    # Calculate total points for the specific student and topic
    total_points = StudentResponse.objects.filter(
        student=instance.student,
        question__topic=instance.question.topic
    ).aggregate(total_points=Sum('points'))['total_points']

    # Update or create the StudentTopicPoints entry
    StudentTopicPoints.objects.update_or_create(
        student=instance.student,
        topic=instance.question.topic,
        defaults={'total_points': total_points}
    )


class StudentOtherData(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE)  # assuming you have a Student model
    date_of_birth = models.DateField()
    math_marks = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 95.50
    science_marks = models.DecimalField(max_digits=5, decimal_places=2)
    social_science_marks = models.DecimalField(max_digits=5, decimal_places=2)
    parental_influence = models.CharField(max_length=255)  # e.g., "High", "Moderate", "Low"
    area_choice = models.CharField(max_length=10, choices=[('urban', 'Urban'), ('rural', 'Rural')])
    parent_education = models.CharField(max_length=255)  # e.g., "High School", "Graduate", "Post Graduate"
    
    def __str__(self):
        return f"{self.student.email} - Other Data"