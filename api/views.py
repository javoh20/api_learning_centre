from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
 
from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *

def is_admin(request):
    if not request.user.is_authenticated:
        return Response(status = status.HTTP_403_FORBIDDEN)

    if not request.user.is_superuser:
        return Response(status = status.HTTP_403_FORBIDDEN)
    
    return True

# Create your views here.
class UsersAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class StudentsAPIView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user')
            user = get_object_or_404(User, pk = user_id)

            group_id = request.data.get('group')
            group = get_object_or_404(Group, pk = group_id)
            
            end_course_data = request.data.get('end_course_data')

            student = Student.objects.create(
                user = user,
                group = group,
                end_course_data = end_course_data,
            )
            student.save()
            serializer = StudentRegSerializer(student)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(str(e),status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentRegSerializer(students, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class GroupsAPIView(APIView):
    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request):
        name = request.data.get('name')
        
        supervisor_id = request.data.get('supervisor')
        supervisor = get_object_or_404(Teacher, pk = supervisor_id)

        room_id = request.data.get('room')
        room = get_object_or_404(Room, pk = room_id)

        group = Group.objects.create(
            name = name,
            supervisor = supervisor,
            room = room
        )
        group.save()
        serializer = GroupSerializer(group)

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class GroupRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class TeachersAPIView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        user = get_object_or_404(User, pk = request.data.get('user'))
        bio = request.data.get('bio')
        phone = request.data.get('phone')
        photo = request.data.get('photo')

        teacher = Teacher.objects.create(
            user = user,
            bio = bio,
            phone = phone,
            photo = photo
        )
        teacher.save()

        serializer = TeacherSerializer(teacher)

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class TeacherRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class RoomsAPIView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
