# Import the required module for text  
# to speech conversion 
from gtts import gTTS 
from playsound import playsound
import time
import pyaudio
import wave
import speech_recognition as sr
from text_emotion import *
import text_emotion
import os 
import random
language = 'en'




questions=[["Hi, thanks for coming in today.Think of me as a friend I do not judge people , I can not because  I am a computer.I will ask a few questions to get us started and please feel free to tell me anything , your answers are totally confidential.   So , how are you doing today? : "],
          ["where are you from : "],
          ["what are some cool things about the place you live : ",
          "what are somethings you really hate about the place you live in : ",
          "how do you feel about the place you live in : "],
          ["what do you do to relax : ",
          "what do you do when you feel tired out : ",
          "How often do you feel tired out for no good reason and what do you in that situation : "],
          ["what do you do when you are annoyed : ",
          "what do you when you fell restless and want to calm down : ",
          "How do you control your temper : "],
          ["when was the last time you argued with someone and what was it about : ",
          "how do you feel in the moment when you argue with somone : ",
          "How often do you indulge in a fight or argument with someone . Can you tell something about the last time you had a argument : "],
          ["who's someone that's been a positive influence in your life. Can you describe about it. : " ,
          "how close are you to your family and friends. : ",
          "What is the most memorable moment of your life that you had with your friends or family : "],
          ["In the past few days have you been so unhappy that you have been crying endlessly : ",
          "Did the thought of harming yourself ever occur to you and what was it for : ",
          "Did you ever scared or panicky for no very good reason in the past few days and why : "],
          ["Is there anything you regret : ",
          "Is the anything which bothers you again and again : " ,
          "Do you feel sad or miserable about something you did : "],
          ["have you ever been diagnosed with depression : ",
          "have you ever faced a situation which has caused a serious impact on your mental health : ",
          "How often do you feel down,depressed or hopeless : "]
           ]

describe=["Can you tell me something more about it",
          "Tell me more about it",
          "like what",
          "I didn't get you . Can you please elaborate"]

positive=["that is great",
         "awesome",
         "that is good",
         "nice",
         "yeah",
         "cool"]
         
neutral=["right",
        "oh",
        "okay",
        "alright"]


def audiototext(audio):        # audiofile to text
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio = r.record(source)
        print ('Done!') 
    text = r.recognize_google(audio)
    
    return text

def newaudioanaly():    # record audio to text automatic pauses :text output
    
    r = sr.Recognizer() 
    # r.energy_threshold = 25
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)
    # try:
    #     print("You said " + r.recognize_google(audio))
    # except sr.UnknownValueError:
    #     print("Could not understand audio")
    # except sr.RequestError as e:
    #     print("Could not request results; {0}".format(e)) 
    transcript = r.recognize_google(audio) 
    print("done")
    return transcript, audio
         


    
    transcript = r.recognize_google(audio)    
   
     
    
def recordaudio(count):     # record audio to text maniual timing delay : audio output
    count += 1
    CHUNK = 1024 
    FORMAT = pyaudio.paInt16 #paInt8
    CHANNELS = 2 
    RATE = 44100 #sample rate
    RECORD_SECONDS = 10   # manual timing.
    stri="audio"+str(count)+".wav"
    WAVE_OUTPUT_FILENAME =stri

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

    print("*recording")
 
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data) # 2 bytes(16 bits) per channel

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return stri   # returns the audio file

def botspeak(i):
    myobj = gTTS(text=i, lang=language, slow=False) 
        # Saving the converted audio in a mp3 file named 
        # welcome 
    str="ques"+i[3:6]+".mp3"
    myobj.save(str) 
        # Playing the converted file 
    

    playsound(str)
    os.remove(str)    
        # os.system("welcome.mp3")


def audio_c_bot():
    myspl = []
    mygender=""
    mypauses=[]
    myratespeech=[]
    myratio=[]
    count = 0
    emotionreport=[]
    sentimentreport=[] 
    var = "audio"+str(count)+".wav"
    count += 1
    botspeak(questions[0][0])
     # create a directory to store the audio chunks. 
    try: 
        os.mkdir('audio_chunks') 
    except(FileExistsError): 
        pass
    # move into the directory to 
    # store the audio files. 
    os.chdir('audio_chunks') 
    #ans=newaudioanaly()
#-------------------------------------------------------------
    
    ans,audio_file=newaudioanaly()
    with open(var, "wb") as f:
        f.write(audio_file.get_wav_data())
    audio_path = os.getcwd()
    print(voice_gender(var[:-4], audio_path))
    myspl.append(voice_speakingTime(var[:-4], audio_path))
    mypauses.append(voice_pauses(var[:-4], audio_path))
    myratespeech.append(voice_rateOfSpeech(var[:-4], audio_path))
    myratio.append(voice_ratio(var[:-4], audio_path))
    os.remove(var)
#-------------------------------------------------------------
    emotionreport.append(emotion(ans))
    sentimentreport.append(list(sentiment(ans)))

    botspeak(questions[1][0])

    var = "audio"+str(count)+".wav"
    count += 1
    ans,audio_file=newaudioanaly()
    with open(var, "wb") as f:
        f.write(audio_file.get_wav_data())
    audio_path = os.getcwd()
    print(voice_gender(var[:-4], audio_path))
    myspl.append(voice_speakingTime(var[:-4], audio_path))
    mypauses.append(voice_pauses(var[:-4], audio_path))
    myratespeech.append(voice_rateOfSpeech(var[:-4], audio_path))
    myratio.append(voice_ratio(var[:-4], audio_path))
    
    os.remove(var)

    emotionreport.append(emotion(ans))
    sentimentreport.append(list(sentiment(ans)))


    for i in range(2,3):
        botspeak(questions[i][random.randint(0,2)])
        #ans=newaudioanaly()
        ans,audio_file=newaudioanaly()
        var = "audio"+str(i)+".wav"
    
        with open(var, "wb") as f:
            f.write(audio_file.get_wav_data())
        print(voice_gender(var[:-4], audio_path))
        mygender=voice_gender(var[:-4], audio_path)
        myspl.append(voice_speakingTime(var[:-4], audio_path))
        mypauses.append(voice_pauses(var[:-4], audio_path))
        myratespeech.append(voice_rateOfSpeech(var[:-4], audio_path))
        myratio.append(voice_ratio(var[:-4], audio_path))

        if(sentiment(ans)[1]>=-0.2 and sentiment(ans)[1]<=0.2):
            botspeak(describe[random.randint(0,len(describe)-1)])
            #ans=newaudioanaly()
            ans,audio_file=newaudioanaly()
            var = "audio"+str(count)+".wav"
            count += 1
            with open(var, "wb") as f:
                f.write(audio_file.get_wav_data())
            print(voice_gender(var[:-4], audio_path))
            myspl.append(voice_speakingTime(var[:-4], audio_path))
            mypauses.append(voice_pauses(var[:-4], audio_path))
            myratespeech.append(voice_rateOfSpeech(var[:-4], audio_path))
            myratio.append(voice_ratio(var[:-4], audio_path))
            os.remove(var)
            if(sentiment(ans)[0]>0.6):
                botspeak(positive[random.randint(0,len(positive)-1)])
                emotionreport.append(emotion(ans))
                sentimentreport.append(list(sentiment(ans)))
            else:
                botspeak(neutral[random.randint(0,len(neutral)-1)])  
                emotionreport.append(emotion(ans))
                sentimentreport.append(list(sentiment(ans)))
        else:
            if(sentiment(ans)[0]>0.6):
                botspeak(positive[random.randint(0,len(positive)-1)])
                emotionreport.append(emotion(ans))
                sentimentreport.append(list(sentiment(ans)))
            else:
                botspeak(neutral[random.randint(0,len(neutral)-1)]) 
                emotionreport.append(emotion(ans))
                sentimentreport.append(list(sentiment(ans)))

    os.chdir('..')
    print(myspl)

    
    return emotionreport,sentimentreport,mygender,mypauses,myratespeech,myratio      


