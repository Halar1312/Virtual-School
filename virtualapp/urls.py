from django.urls import path
from django.contrib import admin
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('startcall/', views.startcall, name='startcall'),

    path('videocall/', views.videocall, name='videocall'),

    path('eyetracking/', views.eyetracking, name='eyetracking'),

    path('video_feed/', views.video_feed, name='video_feed'),

    path('teacherhome/', views.teacherhome, name='teacherhome'),
    path('teacherEvaluation/', views.teacherEvaluation, name='teacherEvaluation'),
    path('studentAssigment/', views.studentAssigment, name='studentAssigment'),
    path('teacherAssigment/', views.teacherAssigment, name='teacherAssigment'),
    path('editor/', views.editor, name='editor'),
    path('delete_document/<int:docid>/',  views.delete_document, name='delete_document'),

    path('course_description/<int:couseId>/',  views.course_description, name='course_description'),


    # path('studenthome/', views.studenthome, name='studenthome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('postAssignment/<int:couseId>/',  views.postAssignment, name='postAssignment'),

    path('submit_assignment/<int:assignmentID>/',  views.submit_assignment, name='submit_assignment'),

    path('submissions_page/<int:assignmentID>/',  views.submissions_page, name='submissions_page'),

    path('student_course_description/<int:couseId>/',  views.student_course_description, name='student_course_description'),

    path('login/', views.login, name='login'),
    path('mycourses/', views.mycourses, name='mycourses'),
    path('logout/', views.logout, name='logout'),
    path('uploadImage/', views.uploadImage, name='uploadImage'),
    path('assignmentPosted/', views.assignmentPosted, name='assignmentPosted'),
    path('attendance/', views.attendance, name='attendance'),
    path('attendancePic/', views.attendancePic, name='attendancePic'),
    path('whiteboard/', views.whiteboard, name='whiteboard'),
    path('schedule/', views.schedule, name='schedule'),
    path('quiz/', views.quiz, name='quiz'),
    path('studentEvaluation/', views.studentEvaluation, name='studentEvaluation'),
    path('teacherCall/', views.teacherCall, name='teacherCall'),

    path('newstudenthome/', views.newstudenthome, name='newstudenthome'),

    re_path(r'^$', views.all_rooms, name="all_rooms"),
    re_path(r'token$', views.token, name="token"),
    re_path(r'/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),

    path('studentsignup/', views.studentsignup, name='studentsignup'),
    path('studentsignup', views.studentsignup, name='studentsignup'),
    path('teachersignup/', views.teachersignup, name='teachersignup'),
    path('teachersignup', views.teachersignup, name='teachersignup'),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
