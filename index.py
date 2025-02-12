import speech_recognition as sr
import pyttsx3
from datasets import load_dataset

# Load the OpenBookQA dataset
dataset = load_dataset("allenai/openbookqa")
train_df = dataset["train"].to_pandas()

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Convert speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand. Please try again.")
        return None
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return None

def get_answer(question):
    """Find the best answer from the dataset."""
    for _, row in train_df.iterrows():
        if question.lower() in row["question_stem"].lower():
            return row["choices"]["text"][0]  # First answer choice
    return "Sorry, I don't have an answer for that."

# Main loop
speak("Hello! Ask me a question from OpenBookQA.")
while True:
    user_question = listen()
    if user_question:
        answer = get_answer(user_question)
        print(f"Answer: {answer}")
        speak(answer)
