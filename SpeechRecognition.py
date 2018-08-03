from gtts import gTTS
import speech_recognition as sr
import os
import re
import requests
import webbrowser
import smtplib
from datetime import time
from datetime import datetime
from datetime import date


def SpeakUp(audio):
    tts = gTTS(text=audio, lang='en-au')
    tts.save('audio.mp3')
    os.system('start audio.mp3')
    

def myCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print('You said: ' + command + '\n')

    except sr.UnknownValueError:
        SpeakUp('Your last command couldn\'t be heard')
        command = myCommand()

    return command


def assistant(command):
    if 'open google' in command:
        SpeakUp('Opening google webpage')
        url = 'https://www.google.com/'
        webbrowser.open(url)
        print('Done!')

    elif 'website' in command:
        reg_ex = re.search('website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
            SpeakUp('Opening your requested website')
        else:
            pass
    elif 'Google search' in command:
        new = 2
        SpeakUp('what would you like searching for?')
        keyword = myCommand()
        url = "https://google.com/?#q="
        webbrowser.open(url+keyword,new=new)
        SpeakUp('Here are some results for your request')
    elif 'open Notepad' in command:
        os.system("start notepad.exe")
        SpeakUp("Opening notepad")
    elif 'open calculator' in command:
        os.system("start calc.exe")
        SpeakUp("opening calculator")
    elif 'open Chrome' in command:
        os.system("start chrome.exe")
        SpeakUp("opening google chrome")
    elif 'time' in command:
        now = datetime.time(datetime.now())
        print("Current time : ",now.strftime("%I:%M %p"))
        SpeakUp(now.strftime("%I:%M %p"))
    elif 'date' in command:
        now = datetime.now()
        print("Current time : ",now.strftime("%d %B %y"))
        SpeakUp(now.strftime("%d %B %y"))
    elif 'what\'s up' in command:
        SpeakUp('Just doing my thing')
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            print(str(res.json()['joke']))
            SpeakUp(str(res.json()['joke']))
        else:
            print('oops!I ran out of jokes')
            SpeakUp('oops!I ran out of jokes')
    elif 'close' in command:
        if 'Chrome' in command:
            app = "chrome.exe"
            os.system("taskkill /f /im "+app)
            SpeakUp('closing Chrome')
        
        elif 'notepad' in command:
            app = "notepad.exe"
            os.system("task'kill /f /im "+app)
            SpeakUp('closing notepad')
        
    elif 'current temperature' in command:
        SpeakUp("of which city?")
        city = myCommand();
        api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
        url = api_address + city
        json_data = requests.get(url).json()
        temp = json_data['main']['temp']
        tempinc = int(temp - 273.15)
        print('Current temperature in ' + city + ' : ' + str(tempinc) + ' celsius')
        SpeakUp('current temperature in '+ city +' is '+ str(tempinc) +' degree celsius')
    elif 'email' in command:
        SpeakUp('Who is the recipient?')
        recipient = myCommand()
        
        if 'Bharat' in recipient:
            SpeakUp('What should I say?')
            content = myCommand()
            server = smtplib.SMTP('smtp.gmail.com', 468)
            server.ehlo()
            server.starttls()
            server.login('','')
            server.sendmail('bharatjb0@gmail.com', 'bharatjb4@gmail.com', content)
            server.close()
            SpeakUp('Email sent.')
        else:
            SpeakUp('I don\'t know what you mean!')

SpeakUp('how can i help you?')

while True:
    assistant(myCommand())
