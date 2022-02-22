from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from  testApp.forms import SignUpForm,RegisterNewCaseForm
from django.http import HttpResponseRedirect
from testApp.models import Case,CaseImages
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
import os

def home_page_view(request):
    return render(request,'testApp/home.html')
@login_required
def add_missing_person_view(request):
    if request.user.is_authenticated:
        username=request.user.username
    if request.method=='POST':
        data=request.POST
        images=request.FILES.getlist('images')
        current_image=images

        current_case=Case.objects.create(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        image=current_image[0],
        user=request.user
        )

        # print(images)
        # for mul_image in images:
        #     CaseImages.objects.create(
        #     case=current_case,
        #     image=mul_image
        #     )
        #     print('creating multiple image object')



        return HttpResponseRedirect('/')

    return render(request,'testApp/user.html',{'username':username})




def getCases_view(request):
    message1='No case has been registered yet'
    #name=request.session['name']
    if request.user.is_authenticated:
        #print(request.user)
        case=Case.objects.filter(user=request.user)
        return render(request,'testApp/viewcases.html',{'cases':case,'message1':message1})
    return render(request,'testApp/viewcases.html')

def about_view(request):
    return render(request,'testApp/about.html')

def logout_view(request):
    return render(request,'testApp/logout.html')
@login_required
def admin_view(request):
    return render(request,'testApp/admin.html')

def signup_view(request):
    form=SignUpForm()
    #print('68')
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            #print('71')

            user=form.save()
            user.set_password(user.password)#for hasing password using user model
            user.save()
            #print('76')
            return HttpResponseRedirect('/accounts/login')
        #print('78')
    #print('80')
    return render(request,'testApp/signup.html',{'form':form})

def sendAlert(request):

    message="The missing person has not been found yet.Please check again and wait for further notifications"
    if request.user.is_authenticated:
        my_file=Path('name_list.txt')
        get_list=[]

        if my_file.exists():
            with open('name_list.txt','rb') as f:
                try:
                    get_list=pickle.load(f)
                except EOFrror:
                    get_list=[]
        myname_list=[]
        for myname in get_list:
            # print(myname)
            filen=os.path.basename(myname)
            # print(filen)
            myname=os.path.splitext(filen)[0]
            # print(myname)
            if not myname=='Unknown':
                myname_list.extend([myname])
        #myname=myname.replace('.jpg','')
        #myname=myname[12:]
        #print(myname_list)
        #case=Case.objects.filter(user=request.user)
        case=Case.objects.filter(name__in=myname_list,user=request.user)

        return render(request,'testApp/alert.html',{'cases':case})
    return render(request,'testApp/alert.html',{'message':message})





import face_recognition
import cv2
import numpy as np
import os
import glob
import pickle
global fac_nam
from pathlib import Path
from django.core.mail import send_mail
# fac_nam="test"
def FC(request):
    faces_encodings = []
    faces_names = []
    cur_direc = os.getcwd()
    path = os.path.join(cur_direc,'static/img/')
    list_of_files = [f for f in glob.glob(path+'*')]
    number_files = len(list_of_files)
    names = list_of_files.copy()


    for i in range(number_files):
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
        globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
        faces_encodings.append(globals()['image_encoding_{}'.format(i)])
    # Create array of known names
        names[i] = names[i].replace(cur_direc, "")
        faces_names.append(names[i])



    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True


    video_capture = cv2.VideoCapture(0)

    while True:
        if number_files==0:
            break
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations( rgb_small_frame)
            face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces (faces_encodings, face_encoding,tolerance=0.5)
                name = "Unknown"
                face_distances = face_recognition.face_distance( faces_encodings, face_encoding)
                #print(face_distances)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = faces_names[best_match_index]
                    # request.session['name']=name
                    #read file
                    #compar file with namesif  yes
                    #if no to write name

                face_names.append(name)
        process_this_frame = not process_this_frame
        global fac_nam
        fac_nam=face_names

        my_file=Path('name_list.txt')
        if my_file.exists():
            with open('name_list.txt','rb') as f:
                try:
                    get_list=pickle.load(f)
                except EOFrror:
                    get_list=[]
        else:
            get_list=[]

        print(get_list)
        if not set(face_names).issubset(get_list):
            message='{} has been found'.format(face_names)
            send_mail('Subject here', message, 'sumitsankar9@gmail.com',
    ['sharat123dewas@gmail.com'], fail_silently=False)
            face_names.extend(get_list)
            with open('name_list.txt','wb') as f:
                pickle.dump(face_names,f)
        # print("found")
        #print(fac_nam)
        # print('test --{}'.format(request.session['name']))
        # sendAlert(face_names)
        # print('face detected --{}'.format(face_names))
    # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    # Input text label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # Display the resulting image
        cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponseRedirect('/')
