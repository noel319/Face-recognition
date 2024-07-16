import cv2
import cv2.cv as cv
import sqlite3
import numpy as np
from Tkinter import *

root=Tk()

detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#detector=cv2.CascadeClassifier('lbpcascade_frontalface.xml')
0cap=cv2.VideoCapture(0)

def insertOrUpdate(db_file):
    conn=sqlite3.connect(db_file)
    cmd="SELECT * FROM Members WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    ifRecordExist=0
    for row in cursor:
        ifRecordExist=1
    if(ifRecordExist==1):
        cmd="UPDATE Members SET Name="+str(Name)+"WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO Members(ID,Name) Values("+str(Id)+","+str(Name)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()
    
    
Id=raw_input('Enter the User ID')
Name=raw_input('Enter the User Name')

database="D:\IOT Project for Semester IV\Program\Face Recognition\Attendance.db"
insertOrUpdate(database)
sampleNum=0;
while(True):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t = cv.GetTickCount()
    faces = detector.detectMultiScale(gray, 1.4, 5)
    t = cv.GetTickCount() - t
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        sampleNum=sampleNum+1
        cv2.imwrite("dataset2/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
        
        cv2.imshow('frame',img)
    if(cv2.waitKey(100) & 0xFF == ord('q')):
        break
    elif(sampleNum>70):
        break
print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
print("Faces Found:",len(faces))
cap.release()
cv2.destroyAllWindows()    
