import ollama
import speech_recognition as sr  
import pyttsx3  
import time  
import webbrowser  
import urllib.parse  
import pywhatkit  
import psutil  
import socket  
import requests  
from datetime import datetime  
  
engine = pyttsx3.init()  
engine.setProperty("rate", 170)  

def speak(text):  
    print("\nFriday.:", text) 
    engine.say(text)  
    engine.runAndWait()  

def listen():  
    r = sr.Recognizer()  
    with sr.Microphone() as source:  
        print("\nListening...")  
        r.adjust_for_ambient_noise(source)  
        try:  
            audio = r.listen(source, timeout=60)   
            command = r.recognize_google(audio).lower()  
            print("You said:", command)  
            return command  
        except sr.UnknownValueError:  
            print("Could not understand, try again.")  
            return None  
        except sr.RequestError:  
            print("Speech Recognition API error.")  
            return None  

def chat_with_jarvis(prompt):  
    try:  
        response = ollama.chat(model="llama3.2:1b", messages=[{"role": "user", "content": prompt + " Summarize within 50 words."}])  
        return response["message"]["content"]  
    except Exception as e:  
        return f"Error: {str(e)}"  

def search_google(query):  
    query = urllib.parse.quote(query)  
    url = f"https://www.google.com/search?q={query}"  
    webbrowser.open(url)  
    speak(f"Searching Google for {query}")  

def play_youtube(video):  
    pywhatkit.playonyt(video)  
    speak(f"Playing {video} on YouTube")  

def get_time():  
    current_time = datetime.now().strftime("%I:%M %p")  
    speak(f"The current time is {current_time}")  

def get_ip():  
    hostname = socket.gethostname()  
    ip_address = socket.gethostbyname(hostname)  
    speak(f"Your IP address is {ip_address}")  

def get_system_usage():  
    cpu_usage = psutil.cpu_percent()  
    ram_usage = psutil.virtual_memory().percent  
    speak(f"CPU usage is at {cpu_usage} percent and RAM usage is at {ram_usage} percent")  

def get_location():  
    try:  
        response = requests.get("http://ip-api.com/json/").json()  
        city = response.get("city", "unknown")  
        country = response.get("country", "unknown")  
        speak(f"You are in {city}, {country}")  
    except Exception as e:  
        speak("I couldn't fetch your location")  

def jarvis():  
    speak("Hello, I am Friday. How can I assist you?")  
    while True:  
        command = listen()  
        if command:  
            if "exit" in command or "quit" in command:  
                speak("Goodbye!")  
                break   
            elif "search" in command:  
                query = command.replace("search", "").strip()  
                if query:  
                    search_google(query)  
            elif "play" in command:  
                video = command.replace("play", "").strip()  
                if video:  
                    play_youtube(video)  
            elif "time" in command:  
                get_time()  
            elif "ip address" in command or "my ip" in command:  
                get_ip()  
            elif "cpu" in command or "ram" in command or "system usage" in command:  
                get_system_usage()  
            elif "where am i" in command or "my location" in command:  
                get_location()  
            else:  
                response = chat_with_jarvis(command)  
                speak(response)  
        time.sleep(1)  

if __name__ == "__main__":  
    jarvis()
