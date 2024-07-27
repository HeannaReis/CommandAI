import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak_text(self, text):
        cleaned_text = self.clean_text(text)
        self.engine.say(cleaned_text)
        self.engine.runAndWait()

    def clean_text(self, text):
        import re
        return re.sub(r'[\*\_\#]', '', text)
