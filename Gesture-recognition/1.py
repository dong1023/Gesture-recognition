import pyttsx3


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)

    engine.say(text)
    engine.runAndWait()

speak('89')