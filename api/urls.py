from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UsersAPIView.as_view()),
    
    path('students/', StudentsAPIView.as_view()),
    path('students/<int:pk>/', StudentRUDAPIView.as_view()),

    path('groups/', GroupsAPIView.as_view()),
    path('groups/<int:pk>/', GroupRUDAPIView.as_view()),

    path('rooms/', RoomsAPIView.as_view()),
    path('rooms/<int:pk>/', RoomRUDAPIView.as_view()),

    path('teachers/', TeachersAPIView.as_view()),
    path('teachers/<int:pk>/', TeacherRUDAPIView.as_view()),
]
