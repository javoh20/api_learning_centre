from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length = 255)
    price_per_month = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)

class Teacher(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    bio = models.TextField()
    phone = models.CharField(max_length = 20, unique=True)
    photo = models.ImageField(upload_to="teachers/")   
    direction = models.ForeignKey(Subject, on_delete = models.SET_NULL, null = True)
    sign_data = models.DateField(auto_now_add = True)
    balance = models.IntegerField(default = 0)
    end_contract_date = models.DateField()

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length = 255)
    supervisor = models.ForeignKey(Teacher, on_delete = models.PROTECT)
    room = models.ForeignKey(Room, on_delete = models.PROTECT)

    def __str__(self):
        return self.name


class Time(models.Model):
    lesson_order = models.IntegerField(unique=True)
    start_time = models.TimeField(unique=True)
    end_time = models.TimeField(unique=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Timelist(models.Model):
    week_days = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    group = models.ForeignKey(Group,on_delete = models.CASCADE,)
    day = models.CharField(max_length = 15, choices = week_days, null = False)
    
    def __str__(self):
        return f"{self.group}, {self.day}"
    
    class Meta:
        unique_together = ('group', 'day')


class Lesson(models.Model):
    timelist = models.ForeignKey(Timelist, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete = models.SET_NULL, null = True)
    teacher = models.ForeignKey(Teacher, on_delete = models.SET_NULL, null = True)
    room = models.ForeignKey(Room, on_delete = models.SET_NULL, null = True)
    time = models.ForeignKey(Time, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return str(f"{self.timelist}, {str(self.subject)}, \n {str(self.time)}")
    
    class Meta:
        unique_together = ('timelist', 'subject', 'teacher', 'room', 'time')


class Student(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 20, unique=True)
    sign_course_data = models.DateField(auto_now_add = True)
    group = models.ForeignKey(Group, on_delete = models.PROTECT)
    end_course_data = models.DateField()
    balance = models.IntegerField(default = 0)
    graduated = models.BooleanField(default = False)

    def __str__(self):
        return self.name


class DeletedStudents(models.Model):
    name = models.CharField(max_length = 255)
    cause = models.CharField(max_length = 255)
    date = models.DateField(auto_now_add = True)


class PaymentHistory(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    date_time = models.DateTimeField(auto_now_add = True)
    payment_amount = models.IntegerField()

    def __str__(self):
        return self.student.name
    
class SalaryHistory(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    date_time = models.DateTimeField(auto_now_add = True)
    payment_amount = models.IntegerField()

    def __str__(self):
        return self.teacher.name