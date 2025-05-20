import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
subject=[]

def say(text):
    engine.say(text)
    engine.runAndWait()

def take_input_subject():
    