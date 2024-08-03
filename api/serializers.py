from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name', 'first_name')

class TeacherShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'photo')

class GroupNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class StudentShortSerializer(serializers.ModelSerializer):
    group = GroupNameSerializer()

    class Meta:
        model = Student
        fields = ('id', 'name', 'group', )

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            last_name = validated_data['last_name'],
            first_name = validated_data['first_name'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user
    
class StudentRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    supervisor = TeacherShortSerializer()

    class Meta:
        model = Group
        fields = ('id', 'name', 'room', 'supervisor', )

class StudentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    group = GroupNameSerializer()
    class Meta:
        model = Student
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = "__all__"

class TimelistSerializer(serializers.ModelSerializer):
    group = GroupNameSerializer()
    class Meta:
        model = Timelist
        fields = ('id', 'day', 'group', )

class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
    

class LessonSerializer(serializers.ModelSerializer):
    timelist = TimelistSerializer()
    subject = SubjectSerializer()
    teacher = TeacherShortSerializer()
    room = RoomSerializer()
    time = TimeSerializer()
    class Meta:
        model = Lesson
        fields = ('id', 'timelist', 'subject', 'teacher', 'room', 'time', )

class PaymentHistorySerializer(serializers.ModelSerializer):
    student = StudentShortSerializer()
    class Meta:
        model = PaymentHistory
        fields = '__all__'

class SalaryHistorySerializer(serializers.ModelSerializer):
    teacher = TeacherShortSerializer()
    class Meta:
        model = SalaryHistory
        fields = '__all__'