from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class RoomShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('number',)

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name', 'first_name')

class TeacherShortSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    class Meta:
        model = Teacher
        fields = ('id', 'user', 'photo')

class GroupNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )

class StudentShortSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    group = GroupNameSerializer()

    class Meta:
        model = Student
        fields = ('id', 'user', 'group', )

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
    user = UserSerializer()
    class Meta:
        model = Student
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Teacher
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    room = RoomShortSerializer()
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