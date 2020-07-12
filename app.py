from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
import MySQLdb
from werkzeug.utils import secure_filename
from flask_mail import Mail
import json
import os 
import math
from datetime import datetime
import audio_record_analysis
import real_time_video
from threading import Thread
from multiprocessing import Process
import multiprocessing
import sys
from flaskthreads import AppContextThread
import mysql.connector
import base64
from flask import jsonify


app = Flask(__name__)
application=app
app.secret_key = 'scb'
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

dict11={}
dict21={}

#app.config['MYSQL_HOST'] = params['host']
#app.config['MYSQL_USER'] = params['usern']
#app.config['MYSQL_PASSWORD'] = params['pass']
#app.config['MYSQL_DB'] =params['db']


#mysql = MySQL(app)
#cur = mysql.connection.cursor()


plopl=1









def f1(dict1):
    
    r1,r2=real_time_video.video_c()
    dict1[0]=r1
    dict1[1]=r2



def f3(dict2):

    r1,r2,r3,r4,r5,r6=audio_record_analysis.audio_c_bot()
    try:
        os.chdir('audio_chunks')
        remove_all()
    except:
        print("Cleaning complete . ")
    # newaudioanaly()
    def remove_all():
        for i in range(0,5):
            fi="audio"+str(i)+".TextGrid"
            os.remove(fi)
            
    dict2[0]=r1
    dict2[1]=r2
    dict2[2]=r3
    dict2[3]=r4
    dict2[4]=r5
    dict2[5]=r6


def f2(dict2)  :
    f3(dict2)
   
    


mydb = MySQLdb.connect(
  host="localhost",
  user="root",
  passwd="",
  database="smart_c_bot"
)

mycursor = mydb.cursor(MySQLdb.cursors.DictCursor)


app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'mbchampyou@gmail.com',
    MAIL_PASSWORD=  'uhugynhcowyjtjop'
)
mail = Mail(app)



def result(dict1,dict2):
    weights=[2,0,2,2,3,4,3,4,4,5]
    polarity_score=[]
    subjectivity_score=0
    
    for j in range(len(dict2[1])):
        polarity_score.append(dict2[1][j][0])
        subjectivity_score+=dict2[1][j][1]

    total_score=[a*b for a,b in zip(polarity_score,weights)]
    text_score=sum(total_score)/len(total_score)
    subjectivity_score=subjectivity_score/len(total_score)
    print("POLARITY SCORE",text_score)

    empath_dict={}
    
    for i in range(len(dict2[0])):
        for j in dict2[0][i]:
            if(j in empath_dict):
                empath_dict[j]+=dict2[0][i][j]
            else:
                empath_dict[j]=dict2[0][i][j]

    for i in empath_dict:
        if(i not in ['cheerfulness','pride','celebration','heroic','optmism']):
            empath_dict[i]*=-1

    empath_score=0
     
    for i in empath_dict:
         empath_score+=empath_dict[i]
         

    empath_score=empath_score/len(dict2[0])
    empath_score=empath_score/10

    print("EMPATH SCORE",empath_score)

    dict11={}
    for i in dict1[0]:
        print("running----------------------------------------")
        if(i=="angry"):
            dict11[i]=(dict1[0][i]*(-0.4))/dict1[1]
        elif(i=="happy"):
            dict11[i]=(dict1[0][i]*(1))/dict1[1]

        elif(i=="neutral"):
            dict11[i]=(dict1[0][i]*(0))/dict1[1]


        elif(i=="disgust"):
            dict11[i]=(dict1[0][i]*(0.1))/dict1[1] 
        elif(i=="surprised"):
            dict11[i]=(dict1[0][i]*(0.2))/dict1[1]
        elif(i=="sad"):
            dict11[i]=(dict1[0][i]*(-1))/dict1[1]
        else:
            dict11[i]=(dict1[0][i]*(-0.6))/dict1[1]
    print(dict11)
    print(dict1[1])
    video_score=0
    for i in dict11:
        video_score+=dict11[i]
    video_score=video_score/7
    print("VIDEO SCORE",video_score)
    total_final_score=(0.6*text_score)+(0.15*video_score)+(0.25*empath_score)

    
    gen=dict2[2];
    pause=sum(dict2[3])/len(dict2[3]);
    ros=sum(dict2[4])/len(dict2[4]);
    strr=dict2[5];
    str1="good"

    print("TOTAL SCORE:",total_final_score)
    print('GENDER ',dict2[2])
    print('PAUSES',sum(dict2[3])/len(dict2[3])) 
    print('RATE OF SPEECH',sum(dict2[4])/len(dict2[4]))  
    print('SPEAKING TIME RATIO',dict2[5]) 
    print("SUBJECTIVITY SCORE",subjectivity_score)

    if(total_final_score<-0.5):
        str1 = "Significantly distressed. Needs some improvement. Try to stay calm. "
        print(str1)
    elif(total_final_score>=-0.5 and total_final_score<0):
        str1 = "Moderately distressed. Freshen up your mind with positive thoughts. "
        print(str1)
    elif(total_final_score>=0 and total_final_score<0.5):
        str1 = "Stable state of mind. Cheer up yourself"
        print(str1)   
    else:
        str1 = "Well balanced state of mind. Cheer up yourself."
        print(str1)     
     
    sendmail(total_final_score,gen,pause,ros,strr,str1,subjectivity_score)





@app.route("/")
def homepage():
    return render_template('homepage.html')

    
 
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   
    if('user' in session):
       return render_template('dashboard.html')


    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('upass')
    


        sql="select * from login_cred"

        mycursor.execute(sql)
        myresult = mycursor.fetchall()    


        f=0
        for x in myresult:
            if(x['username']==username):
                if(x['password']==userpass):
                    session['user'] = username
                    f=1
                    break
    
        if(f==1):
            return render_template('dashboard.html')
        else:
            return render_template('homepage.html' )

    return render_template('homepage.html')


@app.route('/test')  
def continous():
    
    return render_template('testwindow.html' )
      



@app.route('/start-test')
def test():
    manager = multiprocessing.Manager()
    dict1 = manager.dict()
    dict2=manager.dict()
    proc1=Process(target=f1,args=(dict1,))
    proc2=Process(target=f2,args=(dict2,))
    proc1.start()
    proc2.start()
    
    proc2.join()
    proc1.join()




    
    result(dict1,dict2)
    
    
   
    
    

    return "report sent"



@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

@app.route("/viewreports")   
def viewreports():
    return "Reports" 

#@app.route("/sendmail")
def sendmail(r1,r2,r3,r4,r5,r6,r7):
    mail.send_message('YOUR TEST REPORT ',
                          sender='mbchampyou@gmail.com',
                          recipients = 'mohit8826316926@gmail.com'.split(),
                          body ="""
                          HELLO MOHIT 
                          THANKS FOR TAKING TEST 
                          YOUR REPORT IS BELOW:

                          """+"\nFINAL SCORE: "+str(r1)+"\nGENDER: "+str(r2)+"\n AVERAGE PAUSES: "+str(r3)+"\n RATE OF SPEECH: "+str(r4)+"\n SUBJECTIVITY SCORE"+str(r7)+"\n SPEAKING: "+str(r5)+"\nCONCLUSION: "+str(r6)+""" 
                          Okay i think i've asked everything I need to ask. Thanks for sharing your thoughts with me. I appreciate your effort. I promise that all your answers will be confidential.
Challenges are a part of everyday life. They make us stronger and without them life becomes somewhat meaningless because we have nothing to compare the good times to.
These challenges come in many forms. For some, the challenge is doing well at school, for others it is getting to grips with financial worries.
But, regardless of the challenge, facing up to it is key. Doing so will make you feel like you can take care of yourself, it will also make you understand the value of what you have now.
Facing up to challenges and living through them give us the experiences that make up our life..
 """
                          )
    return "done"










app.run(debug=True)