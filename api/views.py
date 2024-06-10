from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *

# Create your views here.
class UserRegAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        form = {
            "username" : '',
            "last_name" : '',
            "first_name" : '',
            "email" : '',
            "password" : '',
        }
        return Response(form, status = status.HTTP_200_OK)
    
class StudentRegAPIView(APIView):
    def post(self, request):
        # if not request.user.is_authenticated:
        #     return Response(status = status.HTTP_403_FORBIDDEN)

        # if not request.user.is_superuser:
        #     return Response(status = status.HTTP_403_FORBIDDEN)

        try:
            user_id = request.data.get('user')
            user = get_object_or_404(User, pk = user_id)

            course_id = request.data.get('course')
            course = get_object_or_404(Course, pk = course_id)
            
            end_course_data = request.data.get('end_course_data')

            student = Student.objects.create(
                user = user,
                course = course,
                end_course_data = end_course_data,
            )
            student.save()

            return Response(student, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(str(e),status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        ex = {
            "user" : '',
            "course" : '',
            "end_course_data" : ''
        }
        return Response(ex, status = status.HTTP_200_OK)