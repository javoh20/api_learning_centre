from django.urls import path
from .views import *

urlpatterns = [
    path('salary/history/<int:pk>/', SalaryHistoryAPIView.as_view()),
    path('salary/', SalaryAPIView.as_view()),

    path('refill/', RefillAPIView.as_view()),

    path('payment/history/<int:pk>/', PaymentHistoryAPIView.as_view()),
    path('payment/<int:pk>/', PaymentAPIView.as_view()),

    path('group_timelist/<int:pk>/', GroupTimelistAPIView.as_view()),

    path('statistics/', StatisticsAPIView.as_view()),
    path('statistics/students/deleted/', StatisticsStudentsDeletedAPIView.as_view()),
    path('statistics/students/new/', StatisticsNewStudentsAPIView.as_view()),

    path('students/', StudentsAPIView.as_view()),
    path('students/<int:pk>/', StudentRUDAPIView.as_view()),
    path('students/debt/', DebtStudentsAPIView.as_view()),
    path('students/delete/', DeleteStudentAPIView.as_view()),

    path('groups/', GroupsAPIView.as_view()),
    path('groups/<int:pk>/', GroupRUDAPIView.as_view()),

    path('rooms/', RoomsAPIView.as_view()),
    path('rooms/<int:pk>/', RoomRUDAPIView.as_view()),

    path('teachers/', TeachersAPIView.as_view()),
    path('teachers/<int:pk>/', TeacherRUDAPIView.as_view()),

    path('subjects/', SubjectsAPIView.as_view()),
    path('subjects/<int:pk>/', SubjectRUDAPIView.as_view()),

    path('times/', TimesAPIView.as_view()),
    path('times/<int:pk>/', TimeRUDAPIView.as_view()),

    path('timelists/', TimeListsAPIView.as_view()),
    path('timelists/<int:pk>/', TimeListRUDAPIView.as_view()),

    path('lessons/', LessonsAPIView.as_view()),
    path('lessons/<int:pk>/', LessonRUDAPIView.as_view()),
]
