from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    sign_course_data = models.DateField(auto_now_add = True)
    course = models.ForeignKey(Course, on_delete = models.PROTECT)
    end_course_data = models.DateField()
    balance = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.user.username

class PaymentHistory(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    date_time = models.DateTimeField(auto_now_add = True)
    payment_amount = models.IntegerField()

    def __str__(self):
        return self.student.user.username

