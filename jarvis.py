import ollama
import speech_recognition as sr  
import pyttsx3  
import os  
import webbrowser  
import time  

# Initialize text-to-speech engine  
engine = pyttsx3.init()  
engine.setProperty("rate", 170)  # Adjust speaking speed  

def speak(text):  
    print("\nJARVIS.:", text)  # Print response to terminal  
    engine.say(text)  
    engine.runAndWait()  

def listen():  
    r = sr.Recognizer()  
    with sr.Microphone() as source:  
        print("\nListening...")  
        r.adjust_for_ambient_noise(source)  # Reduce background noise  
        try:  
            audio = r.listen(source, timeout=60)  # 5-sec timeout  
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
        response = ollama.chat(model="llama3.2:1b", messages=[{"role": "user", "content": prompt}])  
        return response["message"]["content"]  
    except Exception as e:  
        return f"Error: {str(e)}"  

def jarvis():  
    speak("Hello, I am JARVIS. How can I assist you?")  
    while True:  
        command = listen()  
        if command:  
            if "open notepad" in command:  
                speak("Opening Notepad")  
                os.system("notepad")  
            elif "search google for" in command:  
                query = command.replace("search google for", "").strip()  
                speak(f"Searching Google for {query}")  
                webbrowser.open(f"https://www.google.com/search?q={query}")  
            elif "exit" in command or "quit" in command:  
                speak("Goodbye!")  
                break  
            else:  
                response = chat_with_jarvis(command)  # Ask DeepSeek  
                speak(response)  

        time.sleep(1)  # Prevent CPU overload  

if __name__ == "__main__":  
    jarvis()
