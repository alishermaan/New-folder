import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit
import asyncio
import openai
import time
import os
import random
import pyautogui
import pyjokes
import pyperclip
import ctypes

# Setup for TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # male voice

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Hi Ali")

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.energy_threshold = 1 #Adjust as needed
        listener.pause_threshold = 1.2  # or even 1.5
        audio = listener.listen(source)
    try:
        print("Recognizing...")
        command = listener.recognize_google(audio)
        command = command.lower()
        print(f"You said: {command}")
        return command
    except Exception:
        speak("Sorry, I did not get that. Please say that again.")
        return ""

# Example async smart plug control
def control_plug(turn_on=True):
    if turn_on:
        speak("Turning on the light.")
    else:
        speak("Turning off the light.")

def read_emails():
    speak("Checking your unread emails.")
    print("You have 2 unread emails from Alice and Bob.")

def send_whatsapp_msg():
    pywhatkit.sendwhatmsg_instantly("+1234567890", "Hello from Jarvis!")
    speak("WhatsApp message sent!")

def chat_with_gpt(prompt):
    openai.api_key = "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"
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    return answer

def set_reminder(message, delay):
    speak(f"Okay, I will remind you to {message} in {delay} seconds.")
    time.sleep(delay)
    speak(f"Reminder: {message}")

def tell_date():
    today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")

def take_screenshot():
    image = pyautogui.screenshot()
    image.save("screenshot.png")
    speak("Screenshot taken and saved.")

def define_word(word):
    try:
        summary = wikipedia.summary(word, sentences=1)
        speak(summary)
    except Exception:
        speak("Sorry, I couldn't find the definition.")

def get_weather(city="your city"):
    speak(f"Searching weather for {city}")
    pywhatkit.search(f"weather in {city}")

def do_math(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

def set_timer(seconds):
    def timer_thread():
        time.sleep(seconds)
        speak("Time's up!")
    speak(f"Timer started for {seconds} seconds.")


def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def play_local_music():
    music_dir = "path/to/your/music/folder"
    songs = os.listdir(music_dir)
    song = random.choice(songs)
    os.startfile(os.path.join(music_dir, song))
    speak("Playing a random song from your music.")

def lock_screen():
    ctypes.windll.user32.LockWorkStation()
    speak("Locking your computer.")

def copy_text(text):
    pyperclip.copy(text)
    speak("Copied to clipboard.")

def run_jarvis():
    greet_user()
    while True:
        input("Press Enter to activate Jarvis...")
        command = take_command()
        if not command:
            continue

        if "turn on" in command and ("light" in command or "lights" in command):
            control_plug(turn_on=True)

        elif "turn off" in command and ("light" in command or "lights" in command):
            control_plug(turn_on=False)

        elif "wikipedia" in command:
            speak("Searching Wikipedia...")
            topic = command.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(topic, sentences=2)
                speak(result)
            except Exception:
                speak("Sorry, I couldn't find anything on Wikipedia.")

        elif "play" in command:
            song = command.replace("play", "").strip()
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)

        elif "time" in command:
            time_str = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time_str}")

        elif "date" in command:
            tell_date()

        elif "read my emails" in command or "check my emails" in command:
            read_emails()

        elif "send whatsapp" in command:
            send_whatsapp_msg()

        elif "search google for" in command:
            query = command.replace("search google for", "").strip()
            speak(f"Searching Google for {query}")
            pywhatkit.search(query)

        elif "chat with gpt" in command:
            prompt = command.replace("chat with gpt", "").strip()
            answer = chat_with_gpt(prompt)
            speak(answer)

        elif "remind me to" in command:
            parts = command.replace("remind me to", "").split(" in ")
            if len(parts) == 2:
                message = parts[0].strip()
                try:
                    delay = int(parts[1].strip())
                    set_reminder(message, delay)
                except:
                    speak("Sorry, I couldn't understand the time.")

        elif "screenshot" in command:
            take_screenshot()

        elif "define" in command:
            word = command.replace("define", "").strip()
            define_word(word)

        elif "weather" in command:
            get_weather()

        elif "calculate" in command:
            expression = command.replace("calculate", "").strip()
            do_math(expression)

        elif "set timer for" in command:
            try:
                seconds = int(command.replace("set timer for", "").strip())
                set_timer(seconds)
            except:
                speak("Sorry, I couldn't set the timer.")

        elif "tell me a joke" in command:
            tell_joke()

        elif "play music" in command:
            play_local_music()

        elif "lock screen" in command:
            lock_screen()

        elif "copy" in command:
            text = command.replace("copy", "").strip()
            copy_text(text)

        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that. Please try again.")

if __name__ == "__main__":
    run_jarvis()

