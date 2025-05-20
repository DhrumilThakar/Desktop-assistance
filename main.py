import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import wether  # Ensure you have a valid weather module
import todo  # Import your updated todo module
import subprocess
import random
import json
import requests
from bs4 import BeautifulSoup
import wikipedia

def say(text):
    """ Convert text to speech """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def take_input():
    """ Capture user voice input and return as text """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = r.listen(source)
        
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print(f"Error: {e}")
            return ""

def save_reminder(time, task):
    """ Save reminder to a JSON file """
    reminders = []
    try:
        with open('reminders.json', 'r') as f:
            reminders = json.load(f)
    except FileNotFoundError:
        pass
    
    reminders.append({"time": time, "task": task})
    with open('reminders.json', 'w') as f:
        json.dump(reminders, f)

def save_note(note, category="general"):
    """ Save categorized note to a text file """
    with open('notes.txt', 'a') as f:
        f.write(f"[{category}] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {note}\n")

def tell_joke():
    """ Return a random joke from an API """
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke_data = response.json()
            return f"{joke_data['setup']} ... {joke_data['punchline']}"
    except:
        jokes = [
            "Why don't programmers like nature? It has too many bugs!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "Why did the computer go to the doctor? It had a virus!"
        ]
        return random.choice(jokes)

def get_wikipedia_summary(query):
    """ Get summary from Wikipedia """
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "Sorry, I couldn't find information about that."

say("Hello! I'm your AI assistant. How can I help you today?")

while True:
    text = take_input()
    
    if not text:
        continue  # Skip if no input is captured

    # Help Command
    if "help" in text or "what can you do" in text:
        help_text = """
        I can help you with:
        1. Opening websites (say 'open youtube')
        2. Playing music (say 'play love/punjabi/rap')
        3. Checking weather (say 'what's the weather')
        4. Managing tasks (say 'add/remove/show task')
        5. Setting reminders (say 'set reminder')
        6. Taking notes (say 'take note')
        7. System controls (say 'shutdown/restart')
        8. Telling jokes (say 'tell me a joke')
        9. Learning resources (say 'I want to learn DBMS/SE/DCN/DAA')
        10. Wikipedia searches (say 'search for [topic]')
        11. Calculations (say 'calculate [expression]')
        """
        say(help_text)
        print(help_text)
        continue

    # Open Websites
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["instagram", "https://www.instagram.com"],
        ["spotify", "https://www.spotify.com"],
        ["chatgpt", "https://chat.openai.com"],
        ["google", "https://www.google.com"],
        ["github", "https://github.com"]
    ]
    
    for site in sites:
        if f"open {site[0]}" in text:
            say(f"Opening {site[0]}")
            webbrowser.open(site[1])
            break

    # Open Movie Folder
    if "play movie" in text:
        say("Which genre would you prefer? Action, Comedy, Drama, or Random?")
        genre = take_input()
        if genre:
            path = "D:\\Movies"
            if os.path.exists(path):
                if genre.lower() != "random":
                    path = os.path.join(path, genre.capitalize())
                say(f"Opening {genre} movies folder")
                os.startfile(path)
            else:
                say("Sorry, the movies folder doesn't exist")

    # Tell the Time
    if "what's the time" in text or "current time" in text:
        time = datetime.datetime.now().strftime("%I:%M %p")
        date = datetime.datetime.now().strftime("%B %d, %Y")
        say(f"Current time is {time} on {date}")

    # Enhanced Spotify Playlist
    playlist = [
        ["love", "https://open.spotify.com/playlist/3idf0eYheQD7tLn7jzYGZ4"],
        ["punjabi", "https://open.spotify.com/playlist/32V5aPHTyoOZUooYFk8zPc"],
        ["rap", "https://open.spotify.com/playlist/3m6jVaZ6CpTknW2scaECW0"],
        ["god", "https://open.spotify.com/playlist/5969zpiO2zOnjYeEbZH28m"],
        ["study", "https://open.spotify.com/playlist/37i9dQZF1DX8NTLI2TtZa6"],
        ["workout", "https://open.spotify.com/playlist/37i9dQZF1DX70RN3TfWWJh"]
    ]

    for genre in playlist:
        if f"play {genre[0]}" in text:
            say(f"Playing {genre[0]} music")
            webbrowser.open(genre[1])

    # Weather Feature
    if "what's the weather" in text or "weather update" in text:
        say("Can you tell me your current location?")
        location = take_input()

        if location:
            weather_data = wether.get_weather(location)
            if "error" in weather_data:
                say(f"Sorry, I couldn't fetch the weather. {weather_data['error']}")
            else:
                say(f"Current weather in {weather_data['city']} is {weather_data['temperature']}°C, {weather_data['condition']}, Humidity: {weather_data['humidity']}%. The forecast predicts {weather_data.get('forecast', 'similar conditions')} later today.")
        else:
            say("I didn't catch the location.")

    # Enhanced To-Do List
    if "add task" in text:
        say("What's the priority? High, Medium, or Low?")
        priority = take_input()
        todo.add_task(priority=priority)

    if "remove task" in text:
        todo.remove_task()

    if "show my task" in text or "get my task" in text:
        say("Would you like to filter by priority?")
        filter_priority = take_input()
        todo.get_tasks(priority=filter_priority if "yes" in filter_priority else None)

    # Enhanced Reminder System
    if "set reminder" in text:
        say("What would you like me to remind you about?")
        task = take_input()
        if task:
            say("At what time? Please say the time in 24-hour format, for example, 14:30")
            time_str = take_input()
            try:
                time = datetime.datetime.strptime(time_str, "%H:%M").strftime("%H:%M")
                say("Would you like to set this as a recurring reminder? Daily, Weekly, or One-time?")
                recurring = take_input()
                save_reminder(time, {"task": task, "recurring": recurring.lower()})
                say(f"Reminder set for {time} to {task}, recurring {recurring}")
            except ValueError:
                say("Sorry, I couldn't understand the time format. Please try again.")

    # Enhanced Note Taking
    if "take note" in text:
        say("What category would you like to file this under? Work, Personal, Shopping, or General?")
        category = take_input()
        say("What would you like me to note down?")
        note = take_input()
        if note:
            save_note(note, category.lower() if category else "general")
            say(f"I've saved your note under {category if category else 'general'} category")

    # System Controls with Timer Options
    if "shutdown" in text:
        say("Are you sure you want to shutdown the computer? Also, specify time in minutes or say 'now'")
        confirm = take_input()
        if "yes" in confirm or "sure" in confirm:
            try:
                if "now" in confirm:
                    timer = "0"
                else:
                    timer = ''.join(filter(str.isdigit, confirm))
                    if not timer:
                        timer = "60"
                say(f"Shutting down the computer in {timer} minutes")
                subprocess.run(["shutdown", "/s", "/t", str(int(timer)*60)])
            except:
                say("Shutdown cancelled due to invalid input")
        else:
            say("Shutdown cancelled")

    if "restart" in text:
        say("Are you sure you want to restart the computer? Specify time in minutes or say 'now'")
        confirm = take_input()
        if "yes" in confirm or "sure" in confirm:
            try:
                if "now" in confirm:
                    timer = "0"
                else:
                    timer = ''.join(filter(str.isdigit, confirm))
                    if not timer:
                        timer = "60"
                say(f"Restarting the computer in {timer} minutes")
                subprocess.run(["shutdown", "/r", "/t", str(int(timer)*60)])
            except:
                say("Restart cancelled due to invalid input")
        else:
            say("Restart cancelled")

    # Enhanced Fun Interactions
    if "tell me a joke" in text:
        joke = tell_joke()
        say(joke)

    if "how are you" in text:
        responses = [
            "I'm doing great, thank you for asking! How can I assist you today?",
            "I'm excellent! I've been learning new things. What would you like to know?",
            "I'm functioning perfectly! I'm excited to help you with your tasks!"
        ]
        say(random.choice(responses))
    
    # Enhanced Learning Resources
    subject = [
        ["DBMS", "https://youtube.com/playlist?list=PL3R9-um41Jsw8hAUYOfNmWNjUr73H6ee0"],
        ["SE", "https://youtube.com/playlist?list=PLQ-nEJNYlEV29CBLzIDxcogm6CEZjVad2"],
        ["DCN", "https://youtube.com/playlist?list=PLBlnK6fEyqRgMCUAG0XRw78UA8qnv6jEx"],
        ["DAA", "https://youtube.com/playlist?list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O"]
    ]
    
    for s in subject:
        if f"I want to learn {s[0]}" in text:
            say(f"Would you like video tutorials, documentation, or practice problems for {s[0]}?")
            preference = take_input()
            if "video" in preference:
                say(f"Opening video tutorials for {s[0]}")
                webbrowser.open(s[1])
            elif "documentation" in preference:
                say(f"Opening documentation for {s[0]}")
                webbrowser.open(f"https://www.geeksforgeeks.org/{s[0].lower()}-tutorial/")
            elif "practice" in preference:
                say(f"Opening practice problems for {s[0]}")
                webbrowser.open(f"https://www.hackerrank.com/domains/{s[0].lower()}")

    # Wikipedia Search
    if "search for" in text:
        query = text.replace("search for", "").strip()
        say(f"Searching for information about {query}")
        result = get_wikipedia_summary(query)
        say(result)

    # Calculator
    if "calculate" in text:
        expression = text.replace("calculate", "").strip()
        try:
            result = eval(expression)
            say(f"The result is {result}")
        except:
            say("Sorry, I couldn't perform that calculation")

    # Exit Command
    if "exit" in text or "stop" in text or "that's it" in text:
        say("Goodbye! Have a great day!")
        break