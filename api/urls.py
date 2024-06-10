from django.urls import path
from .views import *

urlpatterns = [
    path('user-register/', UserRegAPIView.as_view()),
    path('student-register/', StudentRegAPIView.as_view())
]
