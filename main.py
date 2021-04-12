# first we import all the libraries we need for 1) speech recognition 2)a text to speech, which reads out jarvis communcations
import speech_recognition as sr
#import a time so that we can tell time 
from time import ctime
import time
#since we are importing libraries that require using tools like microphone, we need to use
#the operating system or "import os" so that we can interact with the operating system
import os
#import for google text to speech
from gtts import gTTS
# we import request so that we can make exteral http searches
import requests, json
# import random allows for random number to be created
import random
# this import allows the program to open a webbrowser
import webbrowser
# the playsound import allows us to create an audio file. This keeps the program from opening
# a mp3 player
import playsound
# here is our wikipedia import for searching
import wikipedia
# this library allows texts to be made into speech
import pyttsx3

# assign variables
listening = True
wiki_summary_speech = True
jarvis = "Jarvis said: "
user_name = ""


# this is the listen function.  
def listen():
    # we assign r to the recognizer method. This method recognizes voice from other noice inputs
    r = sr.Recognizer()
    # the microphone method uses the microphone found in the device. Here we are assign the microphone as
    # the primary resource for listening
    with sr.Microphone() as source:
        print(jarvis, "I am listening...")
        # audio variable is assigned the listen method which has the proper resources (microphone and voice recognizer) passed into it
        audio = r.listen(source)
    data = ""
    try:
        # all the magic of 1) identifying a voice 2) using a microphone as a resource 3) converting the audio file into a string is now passed into this variable
        data = r.recognize_google(audio)
        # we see that by printing the variable
        print("You said: " + data)
    # of course it's important to incorporate exception handeling    
    except sr.UnknownValueError:
        print("Jarvis was unable to understand you")
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return data
# a new listening funtion was created in order to save the new speech file into a new variable. 
# But this function works just the same as the father function listen(). See comments on the listen() function
def listen_two(read_data):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(jarvis, "I am listening...")
        audio = r.listen(source)
    read_data = ""
    try:
        read_data = r.recognize_google(audio)
        print("You said: " + read_data)
    except sr.UnknownValueError:
        print("Jarvis was unable to understand you")
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return read_data

# this function is dedicated to searching through wikipedia
def wiki_listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        respond(jarvis, "What would you like to search for?")
        audio = r.listen(source)
    search_data = ""
    read_data = ""
    try:
        search_data = r.recognize_google(audio)
        respond(jarvis, "Searching for " + search_data)
        research_results = wikipedia.page(search_data)
        print(research_results.summary) 
        listen_for_wiki_response(read_data, research_results)   
    except sr.UnknownValueError:
        print("Jarvis was unable to understand you")
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return search_data

#this function is dedicated to user response in wikipedia
# the function is a straight foward if statements for conditional checks with inputed audio file
# note how listen_two() function is used to listen the user every time
def listen_for_wiki_response(read_data, research_results):
    respond(jarvis, "Would you like me to read a summary of your search results?")
    read_data = listen_two(read_data)
    respond(jarvis, "Processing. Just a few seconds")  
    if "yes" in read_data:
        respond(jarvis, research_results.summary)
    if "no" in read_data: 
         respond(jarvis, "Ok. No Problem")
    
        
    respond(jarvis, "Would you like me to save your results to a file?")
    read_data = listen_two(read_data)
    respond(jarvis, "Processing. Just a few seconds")
    if "yes" in read_data:
        create_txt_file(research_results.content)
        respond(jarvis, "Ok. Done.")
    if "no" in read_data: 
         respond(jarvis, "Ok. No Problem")
    
        
    respond(jarvis, "Now that your file has been created, would you like me to present your new file?")
    read_data = listen_two(read_data)
    respond(jarvis, "Processing. Just a few seconds")
    if "yes" in read_data:
        print(research_results.content)
        read_txt_file(research_results.content)
        respond(jarvis, "Ok. Done.")
    if "no" in read_data: 
         respond(jarvis, "Ok. No Problem")  
    
        

# this function is how jarvis speaks. When we call this function
# we asign talk_to_speech with the 'get talk to Speech' (or gTTS) to create a text string
def respond(jarvis, audioString):
    print(jarvis, audioString)
    talk_to_speech = gTTS(text=audioString, lang='en')
    # we create large parameters to keep the limitations low in the audio text file
    r = random.randint (1, 100000000)
    #convert audio file into a string
    audio_file = 'audio-' + str(r) + '.mp3'
    #use the save method to save the audio file in this workspace
    talk_to_speech.save(audio_file)
    #playsound method plays the selected audio file
    playsound.playsound(audio_file)



# audio data is passed in this function. 
# then, we compare the string in data with pre written string comands to give specific 
# instructions to specific commands
def digital_assistant(data):

    #here we nest the if statments by passing an open string "". That way, we can set an else condition outside of the while loop
    if "" in data:
        if "how are you" in data:
            respond(jarvis, "Since I am a computer, I have no feelings, so don't ask. Just kidding. Where is your humor?")
        if "what time is it" in data:
            respond(jarvis, ctime())
        if "stop listening" in data:
            respond(jarvis,"As you wish. I did not want to listen to you anyway. Good bye.")
        # this is a specific request for wikipedia
        if "Wikipedia" in data:
            # designated function for searching audio to text in wikipedia
            wiki_listen()
    # since we can't program every single command, we will make an else for all others and search the web for it
    else:
        respond(jarvis, "I'm not aware of your request. Don't worry, I'll search it for you.")
        print('searching for ' + data)
        #note how we search in the web browser; by using url and google search
        url = 'https://google.com/search?q='+ data
        # then we use webbrowser to open a new webbrowser
        webbrowser.get().open(url)
        respond(jarvis, "Here is what I found.")
    
    

# This is the function that will create a new file for our search.     
def create_txt_file(text_to_write):
    # Open file and place it in append mode.
    open_file_obj = open("essayTwo.txt.encode", "a",encoding="utf-8")
    # now lets write to a file
    open_file_obj.write(text_to_write)

def read_txt_file(text_to_read):
    # start the converter
    converter = pyttsx3.init()
    rate = converter.getProperty('rate')   # getting details of current speaking rate
    print (rate)                            #printing current voice rate
    converter.setProperty('rate', 125)     # setting up new voice rate
    converter.say(text_to_read)
    converter.runAndWait() 
    converter.stop()

# Lets start by having Jarvis introduce himself 
respond(jarvis, "Hello. My name is Jarvis. I will be your assistant for today.")
respond(jarvis, "What can I help you with?")


# we use a while loop to make the condition true
# data gets converted into the listen() function. The listen funtion will take
# the audio and turn the audio into the data varible, which is a string
# the data string is then passed into the digital_assistant function since the condition is true
while listening == True:
        data = listen()
        listening = digital_assistant(data)
    



