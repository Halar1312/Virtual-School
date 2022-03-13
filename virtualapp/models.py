from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class Student(models.Model):
    studentId = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=40)
    uname = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    imageEncodings = models.CharField(max_length=50000)
    profile_pic=models.ImageField(upload_to="",default='ahsan.jpg')

    def __str__(self):
        return self.fname
    class Meta:
        db_table = "student"

class Teacher(models.Model):
    teacherId = models.AutoField(primary_key=True)
    email = models.CharField(max_length=40)
    fname = models.CharField(max_length=40)
    uname = models.CharField(max_length=40)
    password = models.CharField(max_length=40)

    def __str__(self):
        return self.email
    class Meta:
        db_table = "teacher"

class Course(models.Model):
    couseId = models.AutoField(primary_key=True)
    courseCode = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    credits = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING,db_column='teacherId')

    def __str__(self):
        return self.name
    class Meta:
        db_table = "course"

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateField(("Date"), default=datetime.date.today)
    modified_at = models.DateField(("Date"), default=datetime.date.today)
    class Meta:
        db_table = "document"

# class Course_Offer(models.Model):
#         OfferId = models.AutoField(primary_key=True)
#         couseId = models.ForeignKey(Course,on_delete=models.DO_NOTHING,db_column='couseId')
#         teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING,db_column='teacherId')
#         def __str__(self):
#             return self.name
#
#         class Meta:
#             db_table = "Course_Offer"

class RegisteredStudents(models.Model):
        RegID = models.AutoField(primary_key=True)
        courseId= models.IntegerField(default=0)
        studentId= models.IntegerField(default=0)

        class Meta:
            db_table = "RegisteredStudents"

class Assignment(models.Model):
        assignmentID = models.AutoField(primary_key=True)
        name = models.CharField(max_length=30)
        couseId = models.ForeignKey(Course,on_delete=models.DO_NOTHING,db_column='couseId')
        description = models.CharField(max_length=5000)
        file = models.FileField()
        dueDate = models.CharField(max_length=50)
        assignDate = models.CharField(max_length=50)
        assignmentNo= models.IntegerField(default=0)
        def __str__(self):
            return self.name
        class Meta:
            db_table = "assignment"

class Submission(models.Model):
        submissionID = models.AutoField(primary_key=True)
        assignmentId= models.IntegerField(default=0)
        studentId= models.IntegerField(default=0)
        file = models.FileField()
        class Meta:
            db_table = "submission"

class Attendance(models.Model):
        attendanceID = models.AutoField(primary_key=True)
        studentId= models.IntegerField(default=0)
        percentage= models.IntegerField(default=0)
        date = models.CharField(max_length=50)
        status=models.CharField(max_length=50)
        class Meta:
            db_table = "attendance"
