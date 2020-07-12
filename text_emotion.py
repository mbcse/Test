from empath import Empath
emo = Empath()
import re
import matplotlib.pyplot as pyplot
import sys
from textblob import TextBlob
import matplotlib.pyplot as plt
mysp = __import__("my-voice-analysis")


# audio_file is the name of the file in string format and audio_path is the absolute directory of the audio_file
def voice_gender(audio_file, audio_path):
    return mysp.myspgend(audio_file, audio_path)

def voice_pronunciation(audio_file, audio_path):
    return mysp.mysppron(audio_file, audio_path)

def voice_syllables(audio_file, audio_path):
    return mysp.myspsyl(audio_file, audio_path)

def voice_pauses(audio_file, audio_path):
    return mysp.mysppaus(audio_file, audio_path)

def voice_rateOfSpeech(audio_file, audio_path):
    return mysp.myspsr(audio_file, audio_path)

def voice_articulationSpeed(audio_file, audio_path):
    return mysp.myspatc(audio_file, audio_path)

def voice_speakingTime(audio_file, audio_path):
    return mysp.myspst(audio_file, audio_path)

# ratio of the speaking duration to the total speaking duration
def voice_ratio(audio_file, audio_path):
    return mysp.myspbala(audio_file, audio_path)

# returns a pandas dataframe object containing all the parameters and their values
def voice_reportOverall(audio_file, audio_path): 
    return mysp.mysptotal(audio_file, audio_path)

def  emotion(t):
    data=t
    data=data.replace("\n"," ").strip().lower().replace(".","")
    def clean(text):
        
         return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", text).split())


    
    
    
       
    
    data=clean(data)
    d=emo.analyze(data)
    
    #print(d)

    dff={}
    for i in d:
        if(i in ['cheerfullness','pride','celebration','heroic','optimism','violence','hate','emotional','anger','disappointment']):
            dff[i]=d[i]
    return dff        
    #pyplot.pie([float(dff[v]) for v in dff], labels=[str(k) for k in dff],
          #autopct=None)
    #pyplot.show()          


def sentiment(t):
        #polarity = 0
        #positive = 0
        #wpositive = 0
        #spositive = 0
        #negative = 0
        #wnegative = 0
        #snegative = 0
        #neutral = 0

        analysis = TextBlob(t)
            
        s = analysis.sentiment 
        return s

        
        #if (analysis.sentiment.polarity == 0):  
        #        neutral = 1
        #elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
        #        wpositive = 1
        #elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
        #        positive = 1
        #elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
        #        spositive = 1
        #elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
        #        wnegative = 1
        #elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
        #        negative = 1
        #elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
        #        snegative = 1 
                
    
        

        
        #print()
        #print("General Report: ")

       
        #if (polarity == 0):
        #    print("Neutral")
        #elif (polarity > 0 and polarity <= 0.3):
        #    print("Weakly Positive")
        #elif (polarity > 0.3 and polarity <= 0.6):
        #   print("Positive")
        #elif (polarity > 0.6 and polarity <= 1):
        #    print("Strongly Positive")
        #elif (polarity > -0.3 and polarity <= 0):
        #    print("Weakly Negative")
        #elif (polarity > -0.6 and polarity <= -0.3):
        #    print("Negative")
        #elif (polarity > -1 and polarity <= -0.6):
        #    print("Strongly Negative")

        #print()
        #print("Detailed Report: ")
        #print(str(positive) + "% people thought it was positive")
        #print(str(wpositive) + "% people thought it was weakly positive")
        #print(str(spositive) + "% people thought it was strongly positive")
        #print(str(negative) + "% people thought it was negative")
        #print(str(wnegative) + "% people thought it was weakly negative")
        #print(str(snegative) + "% people thought it was strongly negative")
        #print(str(neutral) + "% people thought it was neutral")
  







