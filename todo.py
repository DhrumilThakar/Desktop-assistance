import pyttsx3
import speech_recognition as sr

# Initialize the AI voice
engine = pyttsx3.init()
tasks = []  # List to store tasks

def say(text):
    """Function to make the AI speak"""
    engine.say(text)
    engine.runAndWait()

def take_input():
    """Capture user voice input and return as text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
            return query.lower()
        except Exception as e:
            print(f"Error: {e}")
            return ""

def add_task():
    """Function to add a task using voice"""
    say("What task do you want to add?")
    task = take_input()
    
    if task:
        tasks.append(task)
        say(f"Task added: {task}")
        print(f"✅ Task added: \"{task}\"")
    else:
        say("I didn't catch that. Please try again.")

def remove_task():
    """Function to remove a task using voice"""
    if not tasks:
        say("Your to-do list is empty.")
        return
    
    say("Which task do you want to remove?")
    task = take_input()
    
    if task in tasks:
        tasks.remove(task)
        say(f"Task removed: {task}")
        print(f"❌ Task removed: \"{task}\"")
    else:
        say("Task not found. Please check your list.")
        print("⚠️ Task not found!")

def get_tasks():
    """Function to get the list of tasks"""
    if tasks:
        say("Here are your tasks.")
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. {task}")
            say(f"Task {idx}: {task}")
    else:
        say("Your to-do list is empty.")
        print("📭 Your to-do list is empty.")
    
    return tasks  # Returning tasks in case needed elsewhere
