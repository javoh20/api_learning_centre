from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from datetime import datetime
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
    
class PaymentAPIView(APIView):
    def get(self, request, pk):
        group = get_object_or_404(Group, pk = pk)

        students = []

        for s in Student.objects.filter(group = group):
            group = s.group
            courses = []
            for l in Lesson.objects.filter(timelist__group=group):
                if l.subject:
                    courses.append(l.subject.name)

            courses = list(OrderedDict.fromkeys(courses))
            price = 0

            for c in courses:
                price += get_object_or_404(Subject, name = c).price_per_month

            balance = s.balance - price

            s.balance = balance
            s.save()

            students.append({
                "Name":s.name,
                "Balance":s.balance,
                "Courses":courses,
                "Payment per month":price,
            })

        return Response(students, status=status.HTTP_200_OK)
    

class RefillAPIView(APIView):
    def post(self, request):
        student = get_object_or_404(Student, pk =  request.data.get('student_id'))
        sum = request.data.get('sum')

        student.balance += sum
        student.save()

        payment = PaymentHistory.objects.create(student = student, payment_amount = sum)
        payment.save()

        return Response({
            "Student":student.name,
            "Balance":student.balance,
        }, status = status.HTTP_200_OK)
    

class PaymentHistoryAPIView(APIView):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk = pk)
        payments = PaymentHistory.objects.filter(student = student)
        serializer = PaymentHistorySerializer(payments, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SalaryAPIView(APIView):
    def post(self, request):
        teacher = get_object_or_404(Teacher, pk =  request.data.get('teacher_id'))
        sum = request.data.get('sum')

        salary = SalaryHistory.objects.create(teacher = teacher, payment_amount = sum)
        salary.save()

        return Response({
            "Teacher":teacher.name,
            "Salary":sum,
        }, status = status.HTTP_200_OK)

class SalaryHistoryAPIView(APIView):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk = pk)
        salaries = SalaryHistory.objects.filter(teacher = teacher)
        serializer = SalaryHistorySerializer(salaries, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
class DeleteStudentAPIView(APIView):
    def post(self, request):
        student = get_object_or_404(Student, pk = request.data.get('student_id'))
        cause = request.data.get('cause')
        
        name = student.name

        record = DeletedStudents.objects.create(name = student.name, cause = cause)
        record.save()

        student.delete()
        return Response({
            "Student name":name,
            "Cause":cause
        }, status = status.HTTP_200_OK)
    
class StatisticsStudentsDeletedAPIView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
            deleted_students = DeletedStudents.objects.filter(date__range=[start_date, end_date])
        else:
            deleted_students = DeletedStudents.objects.all()

        stats = {
            'total_deleted': deleted_students.count(),
            'details': [
                {
                    'name': student.name,
                    'cause': student.cause,
                    'date': student.date
                } for student in deleted_students
            ]
        }

        return Response(stats, status=status.HTTP_200_OK)


class StatisticsNewStudentsAPIView(APIView):

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
            new_students = Student.objects.filter(sign_course_data__range=[start_date, end_date])
        else:
            new_students = Student.objects.all()

        stats = {
            'total_new': new_students.count(),
            'details': [
                {
                    'name': student.name,
                    'email': student.email,
                    'phone': student.phone,
                    'sign_course_data': student.sign_course_data,
                    'group': student.group.name,
                    'subjects': list(set(
                        lesson.subject.name for lesson in Lesson.objects.filter(timelist__group=student.group)
                    ))
                } for student in new_students
            ]
        }

        return Response(stats, status=status.HTTP_200_OK)
