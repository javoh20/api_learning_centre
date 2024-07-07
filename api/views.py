from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
 
from collections import OrderedDict

from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *

def is_admin(request):
    if not request.user.is_authenticated:
        return Response(status = status.HTTP_403_FORBIDDEN)

    if not request.user.is_superuser:
        return Response(status = status.HTTP_403_FORBIDDEN)
    
    return True


class StudentsAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentShortSerializer(students, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            phone = request.data.get('phone')

            group_id = request.data.get('group')
            group = get_object_or_404(Group, pk = group_id)
            
            end_course_data = request.data.get('end_course_data')

            student = Student.objects.create(
                name = name,
                email = email,
                phone = phone,
                group = group,
                end_course_data = end_course_data,
            )
            student.save()
            serializer = StudentRegSerializer(student)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(str(e),status = status.HTTP_400_BAD_REQUEST)


class StudentRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer


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
        serializer = TeacherShortSerializer(teachers, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        bio = request.data.get('bio')
        phone = request.data.get('phone')
        photo = request.data.get('photo')

        teacher = Teacher.objects.create(
            name = name, 
            email = email,
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


class SubjectsAPIView(ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer 

class SubjectRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer 


class TimesAPIView(ListCreateAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer 

class TimeRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer


class TimeListsAPIView(APIView):
    def get(self, request):
        timelists = Timelist.objects.all()
        serializer = TimelistSerializer(timelists, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        group = get_object_or_404(Group, pk = request.data.get('group'))
        day = request.data.get('day')

        timelist = Timelist.objects.create(
            group = group,
            day = day
        )
        timelist.save()

        serializer = TimelistSerializer(timelist)

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class TimeListRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Timelist.objects.all()
    serializer_class = TimelistSerializer


class LessonsAPIView(APIView):
    def get(self, request):
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK) 
    
    def post(self, request):
        timelist = get_object_or_404(Timelist, pk = request.data.get('timelist'))
        subject = get_object_or_404(Subject, pk = request.data.get('subject'))
        teacher = get_object_or_404(Teacher, pk = request.data.get('teacher'))
        room = get_object_or_404(Room, pk = request.data.get('room'))
        time = get_object_or_404(Time, pk = request.data.get('time'))

        lesson = Lesson.objects.create(
            timelist = timelist,
            subject = subject,
            teacher = teacher,
            room = room,
            time = time
        )
        lesson.save()
        
        serializer = LessonSerializer(lesson)

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class LessonRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer



class GroupTimelistAPIView(APIView):
    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        group_name = group.name

        lessons = Lesson.objects.filter(timelist__group=group).order_by('time')

        days = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': []
        }

        for i in lessons:
            day = {
                "subject": SubjectSerializer(i.subject).data,
                "teacher": TeacherShortSerializer(i.teacher).data,
                "room": RoomSerializer(i.room).data,
                "time": TimeSerializer(i.time).data, 
            }
            days[i.timelist.day.lower()].append(day)

        return Response(
            {
                "group": group_name,
                "days": days,
            }
        )
    
class StatisticsAPIView(APIView):
    def get(self, request):
        subject_quantity = Subject.objects.count()
        teachers_quantity = Teacher.objects.count()
        groups_quantity = Group.objects.count()
        students_quantity = Student.objects.filter(graduated = False).count()
        students_graduated_quantity = Student.objects.filter(graduated = True).count()

        result = {
            "Subjects" : subject_quantity,
            "Teachers" : teachers_quantity,
            "Groups" : groups_quantity,
            "Students" : students_quantity,
            "Graduated students" : students_graduated_quantity,
        }

        return Response(result, status = status.HTTP_200_OK)

class DebtStudentsAPIView(APIView):
    def get(self, request):
        debt_students = []

        for s in Student.objects.all():
            if s.balance < 0:
                group = s.group
                courses = []
                for l in Lesson.objects.filter(timelist__group=group):
                    if l.subject:
                        courses.append(l.subject.name)

                courses = list(OrderedDict.fromkeys(courses))

                debt_stud = {
                    "Name": s.name,
                    "Courses": courses,
                    "Debt": str(s.balance)
                }

                debt_students.append(debt_stud)
        
        return Response(debt_students, status=status.HTTP_200_OK)