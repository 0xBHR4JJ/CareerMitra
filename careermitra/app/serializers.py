from rest_framework import serializers
from .models import Topic, Question, StudentResponse, Student,StudentTopicPoints,StudentOtherData

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'mobile_no', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Student.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            mobile_no=validated_data['mobile_no']
        )
        return user


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'topic', 'text', 'options', 'points']

class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResponse
        fields = ['id', 'student', 'question', 'answer', 'points']


class StudentTopicPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTopicPoints
        fields = ['student', 'topic', 'total_points']

class StudentOtherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOtherData
        fields = '__all__'