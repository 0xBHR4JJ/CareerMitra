from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('info/', views.get_user_info, name='get_user_info'),
    # Topic URLs
    path('topics/', views.topic_list, name='topic-list'),
    path('topics/<int:pk>/', views.topic_detail, name='topic-detail'),

    # Question URLs
    path('questions/', views.question_list, name='question-list'),
    path('questions/<int:pk>/', views.question_detail, name='question-detail'),

    # StudentResponse URLs
    path('responses/', views.student_response_list, name='student-response-list'),
    path('responses/<int:pk>/', views.student_response_detail, name='student-response-detail'),

    path('questions/topic/<int:topic_id>/', views.get_questions_by_topic, name='get_questions_by_topic'),
    path('student-topic-points/<int:student_id>/', views.get_student_topic_points, name='student-topic-points'),
    path('student-other-data/<int:student_id>/', views.get_student_other_data, name='get_student_other_data'),
    path('student-other-data/', views.create_student_other_data, name='create_student_other_data'),
     path('student-other-data/update/<int:student_id>/', views.update_student_other_data, name='update_student_other_data'),  # PUT only
]
