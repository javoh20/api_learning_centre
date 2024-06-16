from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

class Room(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return self.number

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bio = models.TextField()
    phone = models.CharField(max_length = 20, unique=True)
    photo = models.ImageField(upload_to="teachers/")   
    direction = models.ForeignKey(Subject, on_delete = models.SET_NULL, null = True)
    sign_data = models.DateField(auto_now_add = True)
    balance = models.IntegerField(default = 0)
    end_contract_date = models.DateField()

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length = 255)
    supervisor = models.ForeignKey(Teacher, on_delete = models.PROTECT)
    room = models.ForeignKey(Room, on_delete = models.PROTECT)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    sign_course_data = models.DateField(auto_now_add = True)
    group = models.ForeignKey(Group, on_delete = models.PROTECT)
    end_course_data = models.DateField()
    balance = models.IntegerField(default = 0)
    graduated = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'group')


class PaymentHistory(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    date_time = models.DateTimeField(auto_now_add = True)
    payment_amount = models.IntegerField()

    def __str__(self):
        return self.student.user.username
    
class SalaryHistory(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    date_time = models.DateTimeField(auto_now_add = True)
    payment_amount = models.IntegerField()

    def __str__(self):
        return self.teacher.user.username