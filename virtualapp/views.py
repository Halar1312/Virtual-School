from django.http import HttpResponse,StreamingHttpResponse
from django.shortcuts import render, redirect
from virtualapp.models import Student
from virtualapp.models import Teacher
from virtualapp.models import Course
from virtualapp.models import Submission
from virtualapp.models import Assignment
from virtualapp.models import Attendance
from virtualapp.models import RegisteredStudents
import datetime
import socket, numpy, pickle
from django.http import JsonResponse
from .models import Document
from django.contrib import messages
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json
from twilio.rest import Client
import jwt
# from twilio import TwilioRestException
from twilio.base.exceptions import TwilioRestException
import os
from twilio.jwt.access_token.grants import ChatGrant, VoiceGrant, VideoGrant
from django.contrib.sessions.models import Session
import cv2
import numpy as np
import face_recognition
from tkinter import *
from tkinter import filedialog
from example import EyeTrack
from gaze_tracking import GazeTracking
import time
from datetime import date
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

userEmail=""

# Create your views here.
fake = Faker()
# Faker makes the fake username for communication module
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_client = Client('SKa0bf14463fe57c2c415ecaa912b2cb8d', 'lLQ6kV2EeZ5sPaZAhxmNO6ZP7Ly86W9L','AC51af379d7e9875d40fd97929fa95698a')
encodingImage="empty"
# View for loading index page
def index(request):
    return render(request, 'vc/index.html')
    # return HttpResponse("Hello, world. You're at the polls index.")

#Dashboard view
def dashboard(request):
    return render(request, 'vc/dashboard.html')
    # return HttpResponse("Hello, world. You're at the polls index.")


# View for loading mycourses's dashboard
def teacherAssigment(request):
    # First of all we'll get the teacher object against session id
    for teacher in Teacher.objects.raw('SELECT teacherId,email,password,uname FROM teacher'):
        if((teacher.email == request.session.get('email')) and ((teacher.password == request.session.get('password')))):
            # params = {'students': students}
            query = 'SELECT couseId,name FROM Course WHERE teacherId = %s' % teacher.teacherId
            print(query+ "/////////////////////////////////")
            courses=Course.objects.raw(query)
            # print(courses[0])
            for course in courses:
                print(course.name)
            # form = EmployeeForm(instance=employee)
            params = {'students': teacher,'courses': courses}
            return render(request, 'vc/teacherAssignment.html',params)

def teacherEvaluation(request):
    # First of all we'll get the teacher object against session id

    for teacher in Teacher.objects.raw('SELECT teacherId,email,password,uname FROM teacher'):
        if((teacher.email == request.session.get('email')) and ((teacher.password == request.session.get('password')))):
            # pasrams = {'students': students}
            params = {'students': teacher}
            return render(request, 'vc/teacherEvaluation.html',params)

def studentAssigment(request):
    # First of all we'll get the student object against session id
    print("Student Assignment") #Check whether it came in this loop
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        print("Student Assignment Loop")
        # if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            # SELECT * from `course` where couseId IN (SELECT courseId FROM `registeredstudents` WHERE studentId=1);
        query = 'SELECT * from course where couseId IN (SELECT courseId FROM registeredstudents WHERE studentId=' +str(students.studentId)+')'
        print(query)
        courses=Course.objects.raw(query)
        for course in courses:
            print(course.name)
        params = {'students': students,'courses': courses}
        return render(request, 'vc/studentAssigment.html',params)
    # return HttpResponse("Hello, world. You're at the polls index.")

def uploadImage(request):
    root=Tk()
    file_path = filedialog.askopenfilename()
    root.destroy()
    # print('file--------------------------------------------------',file_path)
    imageToOpen=face_recognition.load_image_file(file_path)
    image=cv2.cvtColor(imageToOpen,cv2.COLOR_BGR2RGB)
    testencodings = face_recognition.face_encodings(image)
    if len(testencodings) > 0:
        encoding = testencodings[0]
    else:
        print("No faces found in the image!")
        quit()
    stringTOReturn = encodingConvertor(encoding)
    print(stringTOReturn)

def createEncoding(file_path):
    imageToOpen=face_recognition.load_image_file(file_path)
    image=cv2.cvtColor(imageToOpen,cv2.COLOR_BGR2RGB)
    testencodings = face_recognition.face_encodings(image)
    if len(testencodings) > 0:
        encoding = testencodings[0]
    else:
        print("No faces found in the image!")
        quit()
    stringTOReturn = encodingConvertor(encoding)
    # print(stringTOReturn)
    return stringTOReturn

def encodingConvertor(encoding):
    String =""
    for i in encoding:
        String+=str(i)
        String+=','
    return String


def assignmentPosted(request):
    if request.method == "POST":
        if request.POST.get('name') and request.POST.get('description') and request.POST.get('dueDate') and request.FILES['myfile']:
            # savercrd = Assignment()
            # savercrd.name = request.POST.get('name')
            # savercrd.description = request.POST.get('description')
            # savercrd.dueDate = request.POST.get('dueDate')
            # savercrd.file = request.POST.get('myfile')
            # savercrd.save()
            # messages.success(request, "New Assignmnet posted")
            return render(request, "vc/teacherAssignment.html")
            # return redirect('vc/studentsignup.html')
    else:
        return render(request, "vc/teacherAssignment.html")
    # return render(request, 'vc/teacherAssignment.html')

def postAssignment(request,couseId):
    # assignment=AssignmentForm
    # First of all we'll get the teacher object against session id
    for students in Teacher.objects.raw('SELECT teacherId,email,password,uname FROM teacher'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            student=students
    print("post")
    if request.method == "GET":
        params = {'students': students,'courseId': couseId}
        return render(request, "vc/postAssignment.html",params)
    else:
        print("came")
        # print(request.POST.get('assignDoc'))
        if request.POST.get('assignmentNo') and request.POST.get('assignmentName') and request.POST.get('assignmentDesc') and request.POST.get('dueDate') and request.FILES['assignDoc']:
            print("Posted assignment")
            print(couseId)
            savercrd = Assignment() #Create an assignment object and add values to it
            savercrd.name = request.POST.get('assignmentName')
            savercrd.assignmentNo = request.POST.get('assignmentNo')
            savercrd.description = request.POST.get('assignmentDesc')
            savercrd.dueDate = request.POST.get('dueDate')
            savercrd.file = request.FILES['assignDoc']
            x = datetime.datetime.now()
            date=str(x.year)+"-"+str(x.month)+"-"+str(x.day)
            savercrd.assignDate = date
            savercrd.couseId = Course.objects.get(pk=couseId)
            savercrd.save()
            course = Course.objects.get(pk=couseId)
            params = {'students': students,'courseId': couseId,'course':course}
            return render(request, "vc/course_description.html",params)


def attendancePic(request):
    print("In Attendance Pic")
    username = request.GET.get('username', None)
    data={'is_taken':'uzair'}
    # if data['is_taken']:
    data['error_message'] = 'A user with this username already exists.'
    # query='SELECT imageEncodings FROM student where email='+userEmail+';'
    # print(query)
    # for students in Student.objects.raw():
    #     userEncodings=students.imageEncodings

    # uzairEncodings=[-0.18992526829242706, 0.020439382642507553, 0.03620827943086624, -0.02404787205159664, -0.07788147777318954, -0.030346710234880447, -0.016850991174578667, -0.08936721086502075, 0.149512380361557, -0.12816494703292847, 0.16258080303668976, -0.0503758043050766, -0.17921298742294312, 0.030863266438245773, -0.03944356366991997, 0.04872337728738785, -0.03072274848818779, -0.11716526746749878, -0.17444178462028503, -0.1420663595199585, -0.006724029779434204, -0.003519464051350951, -0.02758532203733921, 0.018218692392110825, -0.20961934328079224, -0.32197147607803345, -0.061783693730831146, -0.04938749969005585, 0.04010316729545593, -0.05767069756984711, -0.0648980364203453, 0.013866515830159187, -0.20387661457061768, -0.06680689752101898, 0.057203538715839386, 0.12390792369842529, 0.018626248463988304, 0.0053567709401249886, 0.23248976469039917, -0.05134854465723038, -0.1568928211927414, 0.0020556263625621796, 0.16022250056266785, 0.24899445474147797, 0.13321790099143982, 0.10505913197994232, 0.001871597021818161, -0.07744725048542023, 0.11509398370981216, -0.18619966506958008, 0.08830855786800385, 0.09731639921665192, 0.1042591854929924, 0.10971537232398987, 0.06490518152713776, -0.2055649608373642, 0.015463240444660187, 0.14554761350154877, -0.11563950031995773, 0.11056803911924362, 0.05423253774642944, -0.10423636436462402, -0.07789888232946396, -0.04296182468533516, 0.2789463996887207, 0.09462268650531769, -0.1408572793006897, -0.08173491805791855, 0.12736044824123383, -0.1587125062942505, 0.04793161153793335, 0.028067991137504578, -0.07576087862253189, -0.17957809567451477, -0.2581663727760315, 0.13264933228492737, 0.4545379877090454, 0.19837017357349396, -0.16480305790901184, 0.019244056195020676, -0.0411791130900383, -0.033709827810525894, 0.10607149451971054, 0.06999271363019943, -0.15205040574073792, 0.004356618970632553, -0.006924801506102085, 0.09059706330299377, 0.2458745539188385, 0.08505836129188538, -0.010651715099811554, 0.13368725776672363, 0.014574644155800343, 0.0426604226231575, -0.016812670975923538, 0.0410611629486084, -0.19622360169887543, -0.0371520034968853, -0.08774023503065109, 0.03708863630890846, 0.08982614427804947, -0.06650372594594955, 0.09404756128787994, 0.12421707808971405, -0.21242722868919373, 0.14524206519126892, -0.04240524023771286, -0.05578666180372238, 0.02108648419380188, 0.09407642483711243, -0.03991543874144554, -0.05870350822806358, 0.09866324812173843, -0.2618970274925232, 0.1786685585975647, 0.18174715340137482, 0.05334387719631195, 0.21047142148017883, 0.10665905475616455, 0.058797381818294525, 0.09679751098155975, 0.13914290070533752, -0.14093400537967682, -0.06883829087018967, 0.04809446632862091, -0.0704481452703476, 0.15079718828201294, 0.059711672365665436]
    #
    # uzairEncodings1=(-0.18992526829242706, 0.020439382642507553, 0.03620827943086624, -0.02404787205159664, -0.07788147777318954, -0.030346710234880447, -0.016850991174578667, -0.08936721086502075, 0.149512380361557, -0.12816494703292847, 0.16258080303668976, -0.0503758043050766, -0.17921298742294312, 0.030863266438245773, -0.03944356366991997, 0.04872337728738785, -0.03072274848818779, -0.11716526746749878, -0.17444178462028503, -0.1420663595199585, -0.006724029779434204, -0.003519464051350951, -0.02758532203733921, 0.018218692392110825, -0.20961934328079224, -0.32197147607803345, -0.061783693730831146, -0.04938749969005585, 0.04010316729545593, -0.05767069756984711, -0.0648980364203453, 0.013866515830159187, -0.20387661457061768, -0.06680689752101898, 0.057203538715839386, 0.12390792369842529, 0.018626248463988304, 0.0053567709401249886, 0.23248976469039917, -0.05134854465723038, -0.1568928211927414, 0.0020556263625621796, 0.16022250056266785, 0.24899445474147797, 0.13321790099143982, 0.10505913197994232, 0.001871597021818161, -0.07744725048542023, 0.11509398370981216, -0.18619966506958008, 0.08830855786800385, 0.09731639921665192, 0.1042591854929924, 0.10971537232398987, 0.06490518152713776, -0.2055649608373642, 0.015463240444660187, 0.14554761350154877, -0.11563950031995773, 0.11056803911924362, 0.05423253774642944, -0.10423636436462402, -0.07789888232946396, -0.04296182468533516, 0.2789463996887207, 0.09462268650531769, -0.1408572793006897, -0.08173491805791855, 0.12736044824123383, -0.1587125062942505, 0.04793161153793335, 0.028067991137504578, -0.07576087862253189, -0.17957809567451477, -0.2581663727760315, 0.13264933228492737, 0.4545379877090454, 0.19837017357349396, -0.16480305790901184, 0.019244056195020676, -0.0411791130900383, -0.033709827810525894, 0.10607149451971054, 0.06999271363019943, -0.15205040574073792, 0.004356618970632553, -0.006924801506102085, 0.09059706330299377, 0.2458745539188385, 0.08505836129188538, -0.010651715099811554, 0.13368725776672363, 0.014574644155800343, 0.0426604226231575, -0.016812670975923538, 0.0410611629486084, -0.19622360169887543, -0.0371520034968853, -0.08774023503065109, 0.03708863630890846, 0.08982614427804947, -0.06650372594594955, 0.09404756128787994, 0.12421707808971405, -0.21242722868919373, 0.14524206519126892, -0.04240524023771286, -0.05578666180372238, 0.02108648419380188, 0.09407642483711243, -0.03991543874144554, -0.05870350822806358, 0.09866324812173843, -0.2618970274925232, 0.1786685585975647, 0.18174715340137482, 0.05334387719631195, 0.21047142148017883, 0.10665905475616455, 0.058797381818294525, 0.09679751098155975, 0.13914290070533752, -0.14093400537967682, -0.06883829087018967, 0.04809446632862091, -0.0704481452703476, 0.15079718828201294, 0.059711672365665436)

    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            uzairEncodings = students.imageEncodings
            print("SOMETING")
            # print(userEncodings)
            print("Doneeeeeee")
            i=0
            imageEncoding=[]
            s=""
            while(i<len(uzairEncodings)):
                if(uzairEncodings[i]!=','):
                    s+=uzairEncodings[i]
                else:
                    imageEncoding.append(float(s))
                    s=""
                i+=1
            file_path=r'C:\Users\Hp\Downloads\test.png'
            imageToOpen=face_recognition.load_image_file(file_path)
            image=cv2.cvtColor(imageToOpen,cv2.COLOR_BGR2RGB)
            testencodings = face_recognition.face_encodings(image)
            if len(testencodings) > 0:
                encoding = testencodings[0]
            else:
                print("No faces found in the image!")
                data={'is_taken':'No face found'}
                return JsonResponse(data)
            print("USer's encodings")
            print(imageEncoding)
            print("Test encodings")
            print(imageEncoding)
            matches=face_recognition.compare_faces([imageEncoding],encoding)
            faceDis=face_recognition.face_distance([imageEncoding],encoding)
            if(faceDis<0.45):
                data={'is_taken':'Matched'}
            else:
                data={'is_taken':'Not Matched'}
            return JsonResponse(data)

def gazeTrack(studentId):
    #Fisrt it'll established the connection through the socket
    soc=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
    serverip="172.16.49.252"
    serverport=307
# cap = cv2.VideoCapture (0)
    print("Gaze track")
    print(studentId)
    #Get encodings from the database, afterwards it'll be compared
    std = Student.objects.get(pk=studentId)
    print(std.imageEncodings)
    i=0
    imageEncoding=[]
    s=""
    while(i<len(std.imageEncodings)):
        if(std.imageEncodings[i]!=','):
            s+=std.imageEncodings[i]
        else:
            imageEncoding.append(float(s))
            s=""
        i+=1
    encoding=[]
    #Start time duration now
    t1 = datetime.datetime.now().time()
    gaze = GazeTracking()
    # webcam = cv2.VideoCapture(0)
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera # Capturing the frame using opencv

    #initializing all the variables
    centercount=0
    leftcount=0
    rightcount=0
    faceMatch=0
    faceNotMatch=0
    totalcount = 0
    engagementTime=0
    while True:
        # We get a new frame from the webcam
        _,frame = webcam.read()
        kframe=frame
        imgS=cv2.resize(kframe,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
        facesCurFrame=face_recognition.face_locations(imgS)
        encodesCurFrame=face_recognition.face_encodings(imgS,facesCurFrame)
        #Now we'll compare the encoding fetched from the database and taken from the webcam
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches=face_recognition.compare_faces([imageEncoding],encodeFace)
            faceDis=face_recognition.face_distance([imageEncoding],encodeFace)
            if(faceDis<0.45):
                faceMatch+=1
            else:
                faceNotMatch+=1
        # if len(encodesCurFrame) > 0:
        #     encoding = encodesCurFrame[0]
        # else:
        #     print("No faces found in the image!")
        #
        # print("USer's encodings")
        # print(imageEncoding)
        # print("Test encodings")
        # print(encoding)

        # matches=face_recognition.compare_faces(imageEncoding,encoding)
        # faceDis=face_recognition.face_distance(imageEncoding,encoding)
        print("///////////////////////////")
        totalcount=totalcount+1
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)
        frame = gaze.annotated_frame()
        text = ""
        # time_elapsed = time.time() - prev
        # if time_elapsed > 1./frame_rate:
        #     prev = time.time()
        #Values are updated when gaze.refresh function is called.
        if gaze.is_center():
            text = "Center"
            centercount=centercount+1
            engagementTime+=(1/14)
        elif gaze.is_right():
            text = "Right"
            rightcount=rightcount+1
        elif gaze.is_left():
            text = "Left"
            leftcount= leftcount+1
        elif gaze.is_Up ():
            text = "Up"
        elif gaze.is_blinking():
            text = "Blinking"
        # cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 255, 0), 2)
        #Writing on the frame
        cv2.putText(frame, text, (300, 400), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 2)
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (50,400), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 255, 0), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (50, 420), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 255, 0), 1)
        cv2.putText(frame, "Center Count: " + str(centercount), (50, 440), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 255, 0), 1)
        cv2.putText(frame, "Focused Percentage: " + str((centercount/totalcount)*100)+"%", (50,460), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 255, 0), 1)
        ret,buffer = cv2.imencode (".jpg" , frame , [ int (cv2.IMWRITE_JPEG_QUALITY) , 30 ])
        x_as_bytes = pickle.dumps (buffer)
        soc.sendto (x_as_bytes , (serverip , serverport))
        print("Sent Done")
        cv2.imshow("Demo", frame)
        key=cv2.waitKey(1)
        # print(key)
        #Eye tracking will be stopped here
        if key%256 == 27:
            print("Came in check")
            t2 = datetime.datetime.now().time() #Stopped duration
            duration = datetime.datetime.combine(date.min, t2) - datetime.datetime.combine(date.min, t1) #compare times
            # print(duration.minute)
            # print(duration.second)
            #converting duration compored and getting the integers out of it
            duration=str(duration)
            i=0
            hours=""
            minutes=""
            seconds=""
            while(duration[i]!=':'):
                hours+=duration[i]
                i+=1
            i+=1
            while(duration[i]!=':'):
                minutes+=duration[i]
                i+=1
            i+=1
            while(i<len(duration)):
                seconds+=duration[i]
                i+=1
            hours=int(hours)
            minutes=int(minutes)
            seconds=float(seconds)
            minutes=60*minutes
            seconds+=minutes
            # print((seconds/200)*100)
            #Now we'll update the databse
            perc=(engagementTime/seconds)*100+40
            print(duration)
            print(engagementTime)
            print("Printing facial Recognition")
            print(faceMatch)
            print(faceNotMatch)
            dat = datetime.datetime.now().strftime("%m/%d/%Y")#Taking current tim
            savercrd = Attendance()
            savercrd.studentId =studentId
            savercrd.percentage =int(perc)
            savercrd.date =dat
            if(faceMatch>faceNotMatch) and (perc>30):
                savercrd.status = "Present"
            else:
                savercrd.status = "Not Present"
            savercrd.save()
            # print(request.session.get('email'))
            break
        # cv2.imshow("Demo", frame)
        # if cv2.waitKey(1) == 27:
        #     break
        # print("Prnitng")
        # print(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        x = soc.recvfrom (100000000)
        clientip = x [1] [0]
        data = x [0]
        print (data)
        data = pickle.loads (data)
        print (type (data))
        data = cv2.imdecode (data , cv2.IMREAD_COLOR)
        image=data
        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        frame = data[0]
        # print(frame)
        t2 = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.min, t2) - datetime.datetime.combine(date.min, t1)
        print(t1)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # yield("1")
    webcam.release()

def studentEvaluation(request):
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            studentId=students.studentId
            query = 'SELECT * FROM Attendance WHERE studentId = %s' % studentId
            attendances=Attendance.objects.raw(query)
            params = {'students': students,'attendances':attendances}
            return render(request, 'vc/studentEvaluation.html', params)

def gazeTrackTeacher(studentId):
    soc=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    ip="192.168.10.8"
    port=307
    s.bind((ip,port))
    cap = cv2.VideoCapture (0)
    while True:
        x=s.recvfrom(100000000)
        clientip = x[1][0]
        data=x[0]
        print(data)
        data=pickle.loads(data)
        print(type(data))
        print ("host = " , x[0])
        print ("port = " , x[1])
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        # cv2.imshow('In Server', data) #to open image
        #    cap1 = cv2.VideoCapture (0)
        ret,photo1 = cap.read()
        print ("Photo ND Array : ", photo1) #Creating Nd array for photo
        cv2.imshow('Server send',photo1)
        ret,buffer = cv2.imencode (".jpg" , photo1 , [ int (cv2.IMWRITE_JPEG_QUALITY) , 30 ])
        x_as_bytes = pickle.dumps (buffer)
        s.sendto (x_as_bytes ,x[1])
        if cv2.waitKey(1) == 13:
            break
        image=data
        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        frame = data[0]
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # webcam.release()
    cv2.destroyAllWindows()
    cap.release ( )


# View for loading teacher's dashboard page

def whiteboard(request):
    board()
    return render(request, 'vc/whiteboard.html')

def editor(request): #This is view for making the Notes Page
    #First of all we'll get the student object against session of student
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            students= students
    #Get the total documents
    docid = int(request.GET.get('docid', 0))
    documents = Document.objects.all()
    #Check if the request was post or get
    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        if docid > 0:
            document = Document.objects.get(pk=docid)
            document.title = title
            document.content = content
            document.save()
            return redirect('/?docid=%i' % docid)
        else:
            document = Document.objects.create(title=title, content=content)
            return redirect('/editor/?docid=%i' % document.id)
    if docid > 0:
        document = Document.objects.get(pk=docid)
    else:
        document = ''
    #Creating the context parameters
    context = {
        'docid': docid,
        'documents': documents,
        'document': document,
        'students':students
    }
    return render(request, 'vc/editor.html', context)

def delete_document(request, docid):
    #This is the view for deleting the notes
    document = Document.objects.get(pk=docid)
    document.delete()
    # First of all we'll get the student object against session id
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            students= students
    docid = int(request.GET.get('docid', 0))
    documents = Document.objects.all()
    if docid > 0:
        document = Document.objects.get(pk=docid)
    else:
        document = ''
    context = {
        'docid': docid,
        'documents': documents,
        'document': document,
        'students':students
    }
    return render(request,'vc/editor.html',context)

# View for loading student's dashboard
def newstudenthome(request):
    if request.session.has_key('is_logged'):
        # First of all we'll get the student object against session id
        for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
            if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
                student=students
        params = {'students': students}
        print("Is logged in")
        return render(request, 'vc/newstudenthome.html',params)
    return render(request, 'vc/studentsignup.html')
    # return HttpResponse("Hello, world. You're at the polls index.")

def eyetracking(request):
    gazeTrack()
    return render(request, 'vc/whiteboard.html')


def submit_assignment(request,assignmentID):
    #Here student will upload assignment
    #First we'll fetcg student object from the database
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            students= students
    # assignment=AssignmentForm
    print("post")
    #Check if the request is get or post
    if request.method == "GET":
        params = {'students': students,'courseId': assignmentID}
        return render(request, "vc/submit_assignment.html",params)
    else:
        print("came")
        # print(request.POST.get('assignDoc'))
        if request.FILES['assignDoc']:
            savercrd = Submission()
            studentId=1
            for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
                if((students.email == request.POST.get('email')) and ((students.password == request.POST.get('password')))):
                    studentId=students.studentId
            savercrd.studentId=studentId
            savercrd.file = request.FILES['assignDoc']
            savercrd.assignmentId=assignmentID
            savercrd.save()
            params = {'students': students,'courseId': assignmentID}
            return render(request, "vc/student_course_description.html",params)

# @view.route('/video_feed')
def logout(request):
    print("Logging out")
    # return render(request, 'login.html')
    del request.session['is_logged'] #It'll logout the session
    return redirect('login')

# View for loading login page
def login(request):
    print("In login1")
    if request.method == "POST":
        print("Something posted")
        if request.POST.get('email') and request.POST.get('password'):

            #Check if the login request is for he4 teacher table or the student table

            # savercrd = Student()
            for teachers in Teacher.objects.raw('SELECT teacherId, email,password,uname FROM teacher'):
                # print(teachers.email + " printing")
                # print(teachers.password + " printing")
                if((teachers.email == request.POST.get('email')) and ((teachers.password == request.POST.get('password')))):
                    messages.success(request, "New User posted")
                    params = {'name': teachers.uname}
                    print("Teacher found")
                    request.session['is_logged']=True
                    request.session['email']=teachers.email
                    request.session['password']=teachers.password
                    return render(request, "vc/newteacherhome.html", params)
            for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
                # print(teachers.email + " printing")
                # print(teachers.password + " printing")
                if((students.email == request.POST.get('email')) and ((students.password == request.POST.get('password')))):
                    messages.success(request, "New User posted")
                    params = {'students': students}
                    request.session['is_logged']=True
                    request.session['email']=students.email
                    request.session['password']=students.password
                    print("Got student")
                    userEmail=students.email
                    # print(userEmail,"------------------------------------------------")
                    return render(request, "vc/newstudenthome.html", params)
                    # return redirect('studenthome')
    # return redirect('vc/studentsignup.html')
    # else:
    #     return render(request, "vc/studentsignup.html")
    return render(request, 'vc/login.html')
    # return HttpResponse("Hello, world. You're at the polls index.")

# View for loading student signup page
def studentsignup(request):
    print("Signing up")
    if request.method == "POST":
        if request.POST.get('fname') and request.POST.get('uname') and request.POST.get('email') and request.POST.get('password') and  request.FILES['myfile']:
            savercrd = Student()
            savercrd.fname = request.POST.get('fname')
            savercrd.uname = request.POST.get('uname')
            savercrd.email = request.POST.get('email')
            savercrd.password = request.POST.get('password')
            # savercrd.imageEncode=request.POST.get('avatar-2')
            # print(request.POST.get('avatar-2'))
            myfile = request.FILES['myfile']
            print(myfile)
            encodedString=createEncoding(myfile)
            print(encodedString)
            savercrd.imageEncodings=encodedString
            savercrd.profile_pic=request.FILES['myfile']
            savercrd.save()
            messages.success(request, "New User posted")
            return render(request, "vc/newstudenthome.html")
            # return redirect('vc/studentsignup.html')
    else:
        return render(request, "vc/studentsignup.html")

# View for loading teachers signup page
def teachersignup(request):
    if request.method == "POST":
        if request.POST.get('fname') and request.POST.get('uname') and request.POST.get('email') and request.POST.get('password'):
            savercrd = Teacher()
            savercrd.fname = request.POST.get('fname')
            savercrd.uname = request.POST.get('uname')
            savercrd.email = request.POST.get('email')
            savercrd.password = request.POST.get('password')
            savercrd.save()
            messages.success(request, "New User posted")
            return render(request, "vc/newteacherhome.html")
            # return redirect('vc/studentsignup.html')
    else:
        return render(request, "vc/teachersignup.html")

def all_rooms(request):
    #Return all rooms for chat
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

def attendance(request):
    #Return view for attendance
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            params = {'students': students}
            return render(request, "vc/attendance.html", params)

def schedule(request):
    #Return view for schdeule
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            params = {'students': students}
            return render(request, "vc/schedule.html", params)

def mycourses(request):
    print( request.session.get('email'))
    print( request.session.get('password'))
    return render(request, 'vc/mycourses.html')

def course_description(request,couseId):
    #Course Description for teacher
    #First it'll fetch student object from the database
    for students in Teacher.objects.raw('SELECT teacherId,email,password,uname FROM teacher'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            student=students
    query = 'SELECT * FROM Assignment WHERE couseId = %s' % couseId
    assignments=Course.objects.raw(query)
    for a in assignments:
        print(a.assignmentNo)
    course = Course.objects.get(pk=couseId)
    # params = {'courseId': couseId}
    #Passing parameters to the view
    params = {'students': students,'assignments': assignments,'courseId':couseId,'course':course}
    return render(request, 'vc/course_description.html',params)


def student_course_description(request,couseId):
    #Course Description for student
    #First it'll fetch student object from the database
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            student=students
    query = 'SELECT * FROM Assignment WHERE couseId = %s' % couseId
    assignments=Course.objects.raw(query)
    #Print assignment just to check
    for a in assignments:
        print(a.assignmentNo)
    #Passing parameters to the view
    params = {'students': students,'assignments': assignments,'courseId':couseId}
    return render(request, 'vc/student_course_description.html',params)

def submissions_page(request,assignmentID):
    #Submit assignment page in student
    #First it'll fetch student object from the database
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            student=students
    query = 'SELECT submissionID,assignmentId,studentId FROM Submission WHERE assignmentID = %s' % assignmentID
    submissions=Submission.objects.raw(query)
    # for a in submissions:
    #     print(a.assignmentNo)
    params = {'students': students,'submissions': submissions}
    return render(request, 'vc/submissions_page.html',params)

def quiz(request):
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            params = {'students': students}
            return render(request, "vc/quiz.html", params)

    # return render(request, "vc/attendance.html")

def room_detail(request, slug):
    print("Came in details")
    # room = Room.objects.get(slug=slug)
    # return render(request, 'chat/onlineclass.html', {'room': room})

def token(request):
    identity = request.GET.get('identity', fake.user_name())
    device_id = request.GET.get('device', 'default')  # unique device ID
    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)
    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)
    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)
    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8')
    }
    return JsonResponse(response)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def videocall(request):
    print("Trying to login")
    if request.method == "POST":
        print("Trying to login2")
        # username = request.get_json(force=True).get('username')
        username = json.load(request)['username']
        if not username:
            abort(401)
        conversation = get_chatroom('My Room')
        try:
            conversation.participants.create(identity=username)
        except TwilioRestException as exc:
            # do not error if the user is already in the conversation
            if exc.status != 409:
                raise
        token = AccessToken('AC51af379d7e9875d40fd97929fa95698a', 'SKa0bf14463fe57c2c415ecaa912b2cb8d','lLQ6kV2EeZ5sPaZAhxmNO6ZP7Ly86W9L', identity=username)
        token.add_grant(VideoGrant(room='My Room'))
        token.add_grant(ChatGrant(service_sid=conversation.chat_service_sid))
        # print(token.to_jwt())
        print("All things granted")
        response = {
            'conversation_sid': conversation.sid,
            'token': token.to_jwt().decode('utf-8')
        }
        print("All things granted")
    # return {'token': token.to_jwt().decode('utf-8'),
    #         'conversation_sid': conversation.sid}
        return JsonResponse(response)

def get_chatroom(name):
    print("chatroom1")
    for conversation in twilio_client.conversations.conversations.list():
        if conversation.friendly_name == name:
            return conversation
    # a conversation with the given name does not exist ==> create a new one
    return twilio_client.conversations.conversations.create(
        friendly_name=name)
# ngrok http 5000


if __name__ == '__main__':
    app.run(host='0.0.0.0')


from tkinter import *
def callback(*args):
    color=format(variable.get())

def clear(c):
    c.delete('all')

def board():
    canvas_width=800
    canvas_height=600
    def paint(event):
        x1,y1=(event.x-1),(event.y-1)
        x2,y2=(event.x+1),(event.y+1)
        c.create_oval(x1,y1,x2,y2,fill=color,outline=color)
    color='red'
    master=Tk()
    master.title('WhiteBoard')
    menu=Frame(width=250, height=800, bg='white')
    labelmenu=Label(menu, text='Menu')
    labelmenu.pack() #default side='top'
    menu.pack(side=LEFT) #place as far up as possible, fill horiz/vert, expand to fill space unused by parent
    #buttons toggle write, color, size
    Button(menu, text='Clear',bg='black',fg='white',command= lambda: clear(c)).pack()#grid(row=2,column=0)
    variable = StringVar(menu)
    variable.set("Black") # default value
    w = OptionMenu(menu, variable, "Black", "Blue", "Green","Red")
    w.config(bg = "BLACK",fg="WHITE")
    w["menu"].config(bg="Black",fg="WHITE")
    w.pack()
    variable.trace("w",callback)
    c=Canvas(master,width=canvas_width,height=canvas_height,bg='white')
    c.pack(expand=YES,fill=BOTH)
    c.bind('<B1-Motion>',paint)
    message=Label(master,text='Press and Drag to Draw')
    message.pack(side=BOTTOM)
    master.mainloop()



def video_feed(request):
    #This function will return the frame to java script function and is used in the source
    print("Video feed")
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            studentId=students.studentId
    #Gace track is called which will return the frame to the html
    return StreamingHttpResponse(gazeTrack(studentId), content_type='multipart/x-mixed-replace; boundary=frame')


def video_feed_teacher(request):
    print("Video feed Teacher")
    for students in Teacher.objects.raw('SELECT teacherId,email,password,uname FROM teacher'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            studentId=students.studentId
    return StreamingHttpResponse(gazeTrackTeacher(studentId), content_type='multipart/x-mixed-replace; boundary=frame')


def teacherhome(request):
    return render(request, 'vc/newsteacherhome.html')

def startcall(request):
    #It'll fetch student or teacher object from the database depending on the session
    for students in Student.objects.raw('SELECT studentId,email,password,uname FROM student'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            params = {'students': students}
            return render(request, 'vc/call.html', params)
    for students in Teacher.objects.raw('SELECT teacherId,email,password,uname FROM teacher'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            params = {'students': students}
            return render(request, 'vc/call.html', params)
    # return render(request, 'vc/call.html')

def teacherCall(request):
    #View for connecting teacher's call
    #Fetching teacher object from the database
    for students in Teacher.objects.raw('SELECT teacherId,email,password,uname FROM teacher'):
        if((students.email == request.session.get('email')) and ((students.password == request.session.get('password')))):
            params = {'students': students}
            return render(request, 'vc/teacherCall.html', params)

# Referneces
# https://github.com/antoinelame/GazeTracking
# https://www.twilio.com/
# https://opencv.org/
# https://www.djangoproject.com/
