
from django import forms
from virtualapp.models import User
from virtualapp.models import Student
from virtualapp.models import Teacher
from virtualapp.models import Submission
from virtualapp.models import RegisteredStudents
from virtualapp.models import Assignment
from virtualapp.models import Attendance
# from virtualapp.models import



# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"



class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = "__all__"

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = "__all__"

class RegisteredStudentsForm(forms.ModelForm):
    class Meta:
        model = RegisteredStudents
        fields = "__all__"

class Attendance(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"


# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Courses
#         fields = "__all__"
