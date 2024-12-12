from django.contrib.auth import authenticate, login as auth_login
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Topic, Question, StudentResponse,StudentTopicPoints,StudentOtherData
from .serializers import StudentSerializer,StudentOtherDataSerializer, StudentTopicPointsSerializer,StudentTopicPointsSerializer,TopicSerializer, QuestionSerializer, StudentResponseSerializer
from django.db.models import Sum



@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        auth_login(request, user)
        request.session['user_id'] = user.id  # Store user ID in session
        
        return Response({'message': 'Login successful', 'user_id': user.id}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_info(request):
    # Retrieve user_id from query parameters
    user_id = request.GET.get('user_id')
    
    if user_id:
        try:
            # Fetch the user based on the user_id
            user = Student.objects.get(id=user_id)
            serializer = StudentSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)


# Topic APIs

@api_view(['GET', 'POST'])
def topic_list(request):
    if request.method == 'GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # Assuming the topic has a 'name' field that should be unique
        topic_name = request.data.get('name', None)
        if topic_name and Topic.objects.filter(name=topic_name).exists():
            return Response({"message": "Topic already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with creating the new topic if it doesn't exist
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def topic_detail(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response({'message': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        topic.delete()
        return Response({'message': 'Topic deleted'}, status=status.HTTP_204_NO_CONTENT)

# Question APIs

@api_view(['GET', 'POST'])
def question_list(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # Assuming 'text' is the unique field for a question
        question_text = request.data.get('text', None)
        if question_text and Question.objects.filter(text=question_text).exists():
            return Response({"message": "Question already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with creating the new question if it doesn't exist
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response({'message': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        question.delete()
        return Response({'message': 'Question deleted'}, status=status.HTTP_204_NO_CONTENT)

# StudentResponse APIs
@api_view(['GET', 'POST'])
def student_response_list(request):
    if request.method == 'GET':
        # Retrieve all student responses
        responses = StudentResponse.objects.all()
        serializer = StudentResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        student_id = request.data.get('student')
        question_id = request.data.get('question')
        answer = request.data.get('answer')

        # Validate required fields
        if not all([student_id, question_id, answer]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = Question.objects.get(id=question_id)
            options = question.options
            points = question.points
          

            # Find the index of the answer in the options list
            if answer in options:
                
                
                
                answer_points = points[options.index(answer)]
            else:
                return Response({'error': 'Invalid answer'}, status=status.HTTP_400_BAD_REQUEST)

            # Create or update the StudentResponse
            print(answer_points)
            response, created = StudentResponse.objects.update_or_create(
                student_id=student_id,
                question_id=question_id,
                defaults={'answer': answer, 'points': answer_points}
            )

            serializer = StudentResponseSerializer(response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
def student_response_detail(request, pk):
    try:
        response = StudentResponse.objects.get(pk=pk)
    except StudentResponse.DoesNotExist:
        return Response({'message': 'Response not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentResponseSerializer(response)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = StudentResponseSerializer(response, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        response.delete()
        return Response({'message': 'Response deleted'}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def get_student_topic_points(request, student_id):
    # Retrieve the student's topic points
    student_topic_points = StudentTopicPoints.objects.filter(student_id=student_id)
    
    # Serialize the data
    serializer = StudentTopicPointsSerializer(student_topic_points, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_questions_by_topic(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
        questions = Question.objects.filter(topic=topic)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Topic.DoesNotExist:
        return Response({'message': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get Student Other Data by student_id
@api_view(['GET'])
def get_student_other_data(request, student_id):
    try:
        student_other_data = StudentOtherData.objects.get(student__id=student_id)
        serializer = StudentOtherDataSerializer(student_other_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except StudentOtherData.DoesNotExist:
        return Response({'error': 'Student data not found'}, status=status.HTTP_404_NOT_FOUND)

# Create Student Other Data
@api_view(['POST'])
def create_student_other_data(request):
    student_id = request.data.get('student')

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['student'] = student.id  # Ensure student is correctly referenced

    serializer = StudentOtherDataSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Student Other Data
@api_view(['PUT'])
def update_student_other_data(request, student_id):
    try:
        student_other_data = StudentOtherData.objects.get(student__id=student_id)
    except StudentOtherData.DoesNotExist:
        return Response({'error': 'Student data not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = StudentOtherDataSerializer(student_other_data, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

