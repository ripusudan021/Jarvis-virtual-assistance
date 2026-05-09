import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from groq import Groq

r = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def aiprocess(command):
    client = Groq(api_key="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")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # powerful free model
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Cloud."},
            {"role": "user", "content": command}
        ]
    )

    return response.choices[0].message.content

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry,I couldn't fing {song} in your music library")
    else:
        #let groq Handle the request
        output = aiprocess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis")
    while True:
        #Listen for the wake word "JARVIS"
        # obtain audio from the microphone
        # recognize speech using google
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source,timeout=5,phrase_time_limit=5)
            word = r.recognize_google(audio)
            # print(word) debug print to see what's captured
            if "jarvis" in word.lower():
                speak("Ya")
                with sr.Microphone() as source:
                    print("Jarvis Active..")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processcommand(command)

        except sr.WaitTimeoutError:
            print("No speech detected, still listening...")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except Exception as e:
            print(f"Error: {e}")