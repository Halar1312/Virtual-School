from django.db import models
from datetime import date
from django.utils import timezone

# Create your models here.


class Student(models.Model):
    # user_name = models.CharField(max_length=40)
    fname = models.CharField(max_length=40)
    uname = models.CharField(max_length=40)
    email = models.CharField(max_length=40,default='abc')
    password = models.CharField(max_length=40)
    imageEncodings = models.CharField(max_length=50000)
    profile_pic=models.ImageField(upload_to="",default='ahsan.jpg')

    # user_contact = models.CharField(max_length=20)

    def __str__(self):
        return self.fname

    class Meta:
        db_table = "student"


class Teacher(models.Model):
    # user_name = models.CharField(max_length=40)
    fname = models.CharField(max_length=40)
    uname = models.CharField(max_length=40)
    email = models.CharField(max_length=40,default='abc')
    password = models.CharField(max_length=40)
    # user_contact = models.CharField(max_length=20)

    def __str__(self):
        return self.fname

    class Meta:
        db_table = "teacher"


class Courses(models.Model):
    # user_name = models.CharField(max_length=40)
    couseId = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    credits = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    # password = models.CharField(max_length=40)
    # user_contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "courses"


# class Room(models.Model):
#     """Represents chat rooms that users can join"""
#     name = models.CharField(max_length=30)
#     description = models.CharField(max_length=100)
#     slug = models.CharField(max_length=50, unique=True)
#
#     def __str__(self):
#         """Returns human-readable representation of the model instance."""
#         return self.name
class Course_Offer(models.Model):
        OfferId = models.AutoField(primary_key=True,default=0)
        couseId = models.ForeignKey(Courses,on_delete=models.SET_DEFAULT,db_column='couseId')
        teacher = models.ForeignKey(Teacher,on_delete=models.SET_DEFAULT,db_column='email')
        def __str__(self):
            return self.name

        class Meta:
            db_table = "Course_Offer"

class Assignment(models.Model):
        assignmentID = models.AutoField(primary_key=True,default=0)
        name = models.CharField(max_length=30)
        OfferId = models.ForeignKey(Course_Offer,on_delete=models.SET_DEFAULT,db_column='OfferId')
        description = models.CharField(max_length=5000)
        file = models.FileField()
        dueDate = models.CharField(max_length=50)
        assignDate = models.CharField(max_length=50)
        def __str__(self):
            return self.name

        class Meta:
            db_table = "assignment"


            

class registered_course(models.Model):
        RegID = models.AutoField(primary_key=True,default=0)
        student_email = models.ForeignKey(Student,on_delete=models.SET_DEFAULT,db_column='email')
        OfferId = models.ForeignKey(Course_Offer,on_delete=models.SET_DEFAULT,db_column='OfferId')
        Register_Date=models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return self.name

        class Meta:
            db_table = "registered_course"
            unique_together = (('RegID', 'student_email','OfferId'),)
            



class Lecture(models.Model):
        LectureID = models.AutoField(primary_key=True,default=0)
        OfferId = models.ForeignKey(Course_Offer,on_delete=models.SET_DEFAULT,db_column='OfferId')
        teacher = models.ForeignKey(Teacher,on_delete=models.SET_DEFAULT,db_column='email')
        Lecture_Date=models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return self.name

        class Meta:
            db_table = "Lecture"
            unique_together = (('LectureID', 'OfferId','teacher'),)
            

class Attendence(models.Model):
        AttendenceID = models.AutoField(primary_key=True,default=0)
        student_email = models.ForeignKey(Student,on_delete=models.SET_DEFAULT,db_column='email')
        LectureId = models.ForeignKey(Lecture,on_delete=models.SET_DEFAULT,db_column='LectureId')
        
        def __str__(self):
            return self.name

        class Meta:
            db_table = "Attendence"
            unique_together = (('AttendenceID', 'student_email','LectureId'),)
