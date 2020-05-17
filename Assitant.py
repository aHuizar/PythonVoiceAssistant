import speech_recognition as sr
import webbrowser
from time import ctime
import playsound
import os
from gtts import gTTS


def in_string(terms, string):
    for term in terms:
        if term in string:
            return True
    return False


class Assistant:
    def __init__(self, name):
        self.recognizer = sr.Recognizer()
        self.name = name

    def speak(self, audio_string):
        tts = gTTS(text=audio_string, lang="en")
        audio_file = "audio.mp3"
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(audio_string)
        os.remove(audio_file)

    def listen(self, ask=""):
        with sr.Microphone() as source:
            if ask:
                self.speak(ask)
            try:
                audio = self.recognizer.listen(source, 4, 4)
                voicedata = ""
                try:
                    voicedata = self.recognizer.recognize_google(audio)
                except sr.UnknownValueError:  # random noise
                    self.speak("Sorry, I didn't get that.")
                except sr.RequestError:
                    self.speak("Sorry, my speech service is down")
                print(">>", voicedata.lower())
                return voicedata
            except sr.WaitTimeoutError:
                print("Waiting...")

    def respond(self, string):
        string = string.lower()
        # time
        if in_string(["what's the time", "what time is it", "tell time"], string):
            string_to_speak = ctime().split(" ")[3]  # grab the time component we care about
            am_or_pm = "PM" if int(string_to_speak.split(":")[0]) >= 12 else "AM"  # is is am or pm
            string_to_speak = string_to_speak.split(":")[0] + ":" + string_to_speak.split(":")[
                1] + " " + am_or_pm  # concat
            self.speak(string_to_speak)  # speak
        # searching
        elif in_string(["search for", "google"], string):
            string = string.replace("search for", "")
            string = string.replace("google", "")
            url = "https://google.com/search?q=" + string
            webbrowser.get().open(url)
            self.speak("Here's what I found")
        # location
        elif in_string(["find", "locate", "where's", "where is"], string):
            string = string.replace("find", "").replace("locate", "").replace("where's", "").replace("where is", "")
            url = "https://google.nl/maps/search/" + string + "/&amp;"
            webbrowser.get().open(url)
            self.speak("Here's what I found")
        # say name
        elif in_string(["what's your name", "say your name", "who are you"], string):
            self.speak("My name is " + str(self.name))
        elif in_string(["your new name is", "you're now called"], string):
            string = string.replace("your new name is").replace("you're now called", "")
            self.speak("Okay, my new name is " + string)
            self.name = string
        # exit
        elif in_string(["exit", "bye", "see you later", "quit"], string):
            self.speak("Goodbye!")
            exit()

alexa = Assistant("Alexa")

alexa.speak("How may I help you?")
while 1:
    voice_data = alexa.listen()
    if voice_data is not None:
        alexa.respond(voice_data)
