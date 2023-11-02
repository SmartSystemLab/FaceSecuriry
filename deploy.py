from flask import Flask,url_for, redirect,Response,render_template
import numpy as np 
#from wtforms import FileField,SubmitField
#from tensorflow.keras.models import load_model
import pandas as pd 
#import joblib
#from flask_wtf import FlaskForm
from matplotlib.image import imread
import datetime
import cv2
import time
import os,pickle
import face_recognition

app = Flask(__name__)
app.config["SECRET_KEY"] = "MEEEEEE"
#flower_scaler= joblib.load("iris_scd.pkl")
with open("a.pkl", 'rb') as b:
    encodings = pickle.load(b)


codes = list(encodings.values())

def encode(img):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    code = face_recognition.face_encodings(rgb_img)[0]
    return code



data_table = []

import pandas as pd
def Make_Attendance():
    columns =["Name","Sign_in","Sign_Out","Day","Month","Year","seconds_spent","Minutes_spent","Hours_spent"]
    now = datetime.datetime.now()
    save_date = str(now.day)+"_"+str(now.month)+"_"+str(now.year)
    
    
    first = pd.DataFrame( data_table, columns = ["Label","Time"])

    second_data = []
    for name in first['Label'].unique():
        if name== 'nil' or name =='Unknown':
            continue


        lanre = first[first['Label'] == name]

        
        begin =lanre['Time'].iloc[0]
        #print(begin,name)
        end = lanre['Time'].iloc[len(lanre)-1]

        time2= end.strftime('%I:%M %p')
        time1= begin.strftime('%I:%M %p')
        day,month,day2,time,year = begin.ctime().split(' ')
        day  =day + " "+ day2
        total_time = end-begin

        sec = total_time.total_seconds()

        minutes = sec/60
        hours = minutes/60

        second_data.append([name,time1,time2,day,month,year,sec,minutes,hours])

    second = pd.DataFrame(second_data,columns=columns)
#     second.head()
    second.to_csv("Attendance"+save_date+".csv")
    return second


data_table = []
import time
codes = list(encod.values())
data_table = []
def detect_frame(frame):
    info = [] 
    img = frame.copy()

    #small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    small_frame = img
    color = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)   
    rects = face_recognition.face_locations(color) # face locations
    unknown_encoding  = face_recognition.face_encodings(img,rects)
    #print(len(codes))
    
    for encodings in unknown_encoding:

        code = face_recognition.api.compare_faces(codes,encodings,tolerance = 0.45)
        dist = face_recognition.face_distance(codes,encodings)

        m = dist.argmin()
        if code[m]:
            name= list(encod.keys())[m]

            time = datetime.datetime.now()
        else:
            name= 'Unknown'
            time = datetime.datetime.now()
            
        info.append([name,time])
        data_table.append([name,time])
    
    Make_Attendance()
    return rects,info
    
    
data_table = []

import time
import cv2
def extract_video(video):
    # Same command function as streaming, its just now we pass in the file path, nice!
    cap = cv2.VideoCapture(video)
   
    if cap.isOpened()== False: 
        print("Error opening the video file. Please double check your file path for typos. Or move the movie file to the same location as this script/notebook")

#     while cap.isOpened():
    while True:
        ret, frame = cap.read()

#         # If we got frames, show them.
        if ret == True:
            locations,info =detect_frame(frame)

            for loc,info in zip(locations,info):
                y1, x2, y2, x1 = loc[0], loc[1], loc[2], loc[3]
                name = info[0].split("_")[0]
                if name == 'Unknown':
                    cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
                else:
                    cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200,0 ), 3)


            rec,uffer = cv2.imencode(".jpg",frame)
            frame = uffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
            



@app.route('/')
def video():
    
    file= ''
    print(f"extracting: {file}")
    return Response(extract_video(file), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attendance')
def table():

    now = datetime.datetime.now()
    save_date = str(now.day)+"_"+str(now.month)+"_"+str(now.year)  
    data = pd.read_csv("Attendance"+save_date+ ".csv", index_col = 'Unnamed: 0')  
    return render_template("table.html",tables = [data.to_html()],titles = [""])

if __name__ == '__main__':
    app.run()
