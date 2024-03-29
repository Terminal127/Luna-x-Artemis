import speech_recognition as sr
import whatsapp
import logging
import utils
from RealtimeTTS import TextToAudioStream, AzureEngine
from datetime import datetime
from playsound import playsound
import tempaudiofile
import sys

# import pyttsx3
# import threading

class ContinuousRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = AzureEngine("0b056629cf414956afb50b976d4c5487", "eastus", "en-US-AmberNeural", rate=15.0)
        self.stream = TextToAudioStream(self.engine)
        self.speech_synthesizer = self.engine.get_synthesizer()
        self.speech_config = self.engine.get_speech_config()
        self.connection = None

        # self.recognition_thread = threading.Thread(target=self.continuous_recognition_thread, daemon=True)
        # self.recognition_thread.start()

    def recognize_speech(self):
        try:
            with sr.Microphone() as source:
                print("Speak into your microphone. Press 'Ctrl+C' to exit.")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)

            result = self.recognizer.recognize_google(audio)
            print("Recognized: {}".format(result))

            # Handle recognized speech in a separate function
            self.handle_recognized_speech(result.lower())

        except Exception as e:
            logging.error(f"Error during speech recognition: {e}")

    def handle_recognized_speech(self, recognized_text):
        if "whatsapp" in recognized_text:
            self.handle_whatsapp()
        elif "open" in recognized_text:
            self.handle_apps_open(recognized_text)
        elif "close" in recognized_text:
            self.handle_apps_close(recognized_text)
        elif "hello" in recognized_text and "can you hear" in recognized_text:
            self.luna_response_check()
        elif "sleep" in recognized_text:
            self.handle_sleep()
        elif "shut down" in recognized_text:
            self.handle_shutdown()
        elif "initiate" in recognized_text and "hand" in recognized_text and "gesture" in recognized_text:
            playsound(gesture_response)
            self.handle_gesture()

    def all_audio_initialise(self):
        tempaudiofile.cleanup()
        name = tempaudiofile.whatsapp_speech()
        return name

    def speakpyttsx3(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    # def establish_preconnection(self):
    #     self.synthesizer = speechsdk.SpeechSynthesizer(self.speech_config, None)
    #     self.connection = speechsdk.Connection.from_speech_synthesizer(self.synthesizer)
    #     self.connection.open(True)

    def greet_user(self):
        hour = datetime.now().hour
        if 6 <= hour < 12:
            self.speak_text("Good Morning")
        elif 12 <= hour < 16:
            self.speak_text("Good afternoon")
        elif 16 <= hour < 19:
            self.speak_text("Good Evening")

    def speak_text(self, text):
        try:
            self.speech_synthesizer.speak_text_async(text).get()
        except Exception as e:
            logging.error(f"Error while speaking text: {e}")

    def handle_whatsapp(self):
        playsound(whatsapp)
        self.speak_text("This part is very important! Say 'contact' and then the name of the person you want to send the text.")

        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source)

            query = self.recognizer.recognize_google(audio)
            print(query.lower())

            if "contact" in query.lower():
                name = query.lower().replace("contact", "").strip().replace(".", "").strip()
                if name:
                    folder_path = "C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna\\test"
                    whatsapp.send_files_in_folder(folder_path, name)
        except Exception as e:
            logging.error(f"Error during WhatsApp handling: {e}")

    def luna_response_check(self):
        playsound(luna)
        pass  

    def handle_apps_open(self, app):
        name = app.replace("open", "").strip().replace(".", "").strip()
        text = f"opening {name}"
        self.speak_text(text)
        char_iterator = iter(text)
        self.stream.feed(char_iterator)
        self.stream.play_async()
        if name:
            utils.open_app(name)

    def handle_apps_close(self, app):
        name = app.replace("close", "").strip().replace(".", "").strip()
        text = f"closing {name}"
        self.speak_text(text)
        char_iterator = iter(text)
        self.stream.feed(char_iterator)
        self.stream.play_async()
        if name:
            utils.close_app(name)

    def handle_gesture(self):
        utils.gesture_mode()

    def continuous_recognition_thread(self):
        try:
            playsound(initial_response)
            print("Speak into your microphone. Press 'Ctrl+C' to exit.")

            while True:
                # Only the speech recognition part runs in this separate thread
                self.recognize_speech()

        except KeyboardInterrupt:
            print("Recognition loop terminated.")
            sys.exit("exiting...")

    def handle_sleep(self):
        self.speak_text("Going to sleep. Say 'Hello Luna' to wake me up.")
        self.stream.close()
        sys.exit("exiting...")

    def handle_shutdown(self):
        self.speak_text("Goodbye! Have a nice day")
        sys.exit("exiting...")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    tempaudiofile.cleanup()
    recognition = ContinuousRecognition()
    whatsapp = tempaudiofile.whatsapp_speech()
    tempaudiofile.change_speed(whatsapp, speed=1.2)
    luna = tempaudiofile.luna_speech()
    tempaudiofile.change_speed(luna, speed=1.2)
    initial_response = tempaudiofile.initial_response()
    tempaudiofile.change_speed(initial_response, speed=1.2)
    gesture_response = tempaudiofile.gesture_response()
    tempaudiofile.change_speed(gesture_response, speed=1.2)
    recognition.greet_user()
    recognition.continuous_recognition_thread()
    recognition.stream.close()
    tempaudiofile.cleanup()
    sys.exit("exiting...")
