import cv2 as cv
import sqlite3
import numpy as np
from tkinter import *

root=Tk()

detector=cv.CascadeClassifier('haarcascade_frontalface_default.xml')
#detector=cv2.CascadeClassifier('lbpcascade_frontalface.xml')
cap=cv.VideoCapture(0)

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
    
    
Id=input('Enter the User ID:')
Name=input('Enter the User Name:')

database= r"D:\work\AI\Face recognition\Attendance.db"
insertOrUpdate(database)
sampleNum=0
while(True):
    ret, img = cap.read()
    gray = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t = cv.GetTickCount()
    faces = detector.detectMultiScale(gray, 1.4, 5)
    t = cv.GetTickCount() - t
    for (x,y,w,h) in faces:
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        sampleNum=sampleNum+1
        cv.imwrite("dataset2/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
        
        cv.imshow('frame',img)
    if(cv.waitKey(100) & 0xFF == ord('q')):
        break
    elif(sampleNum>70):
        break
print("detection time = %gms" % (t/(cv.GetTickFrequency()*1000.)))
print("Faces Found:",len(faces))
cap.release()
cv.destroyAllWindows()    
