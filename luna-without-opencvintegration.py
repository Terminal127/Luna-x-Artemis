import azure.cognitiveservices.speech as speechsdk
import whatsapp
import logging
import modules.tensorlessutils as ut
import pyttsx3
from datetime import datetime
from playsound import playsound
import tempaudiofile
import sys
import threading
import time
import pyautogui
import tabs_handler
from selenium import webdriver
import http.client
import json
import darkmode
import genai
import misc.whatsapp_message as wp
import misc.timetable_get as tb
import asyncio
import voicetype as vc
import misc.spotify as ms
import apisgoogle.staticmaps as gapi
import requests

whatsapp = None
luna = None
initial_response = None
gesture_response = None
proxy_send = None
ask_boss = None
app_close = None
sleep_mode =  None
wake_mode = None
voicetype_mode = None
voicetype_mode_stop = None
voicetype_mode_pause = None



class ContinuousRecognition:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(
            subscription='', region='eastus'
        )

        # Set the default voice and language
        self.stream = TextToAudioStream(self.engine)
        self.speech_config.speech_recognition_language = "en-IN"

        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=self.audio_config
        )
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=self.audio_config
        )
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('rate', 190)
        self.engine.setProperty('volume', 1.0)
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        
        
    async def recognize_speech(self):
        try:
            while True:

                result = self.speech_recognizer.recognize_once_async().get()

                

                if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    
                    print("Recognized: {}".format(result.text)) 


                    # WhatsApp functionality
                    # if "whatsapp" in result.text.lower():
                    #     self.handle_whatsapp()
                        
                    if "open" in result.text.lower():
                        # thread = threading.Thread(target=self.handle_apps_open,args=(result.text.lower(),))
                        # thread.start()
                        # thread.join()
                        await self.handle_apps_open_async(result.text.lower())
                    
                    elif "close" in result.text.lower():
                        # thread = threading.Thread(target=self.handle_apps_close,args=(result.text.lower(),))
                        # thread.start()
                        # thread.join()
                        await self.handle_apps_close_async(result.text.lower())
                    
                    elif "show me a map of" in result.text.lower() or " map of" in result.text.lower()or "display a map of" in result.text.lower():
                        location = result.text.lower().replace("show me a map of", "").replace("map of", "").replace("display a map of", "").strip().replace(".", "").strip()
                        gapi.getmap(location, 10)
                        gapi.open_photo()
                    
                    
                    elif "hello"  in result.text.lower():
                        thread = threading.Thread(target=self.luna_response_check)
                        thread.start()
                        thread.join()
                        
                    elif "sleep" in result.text.lower():
                        thread_sleep = threading.Thread(target=playsound,args=(sleep_mode,))
                        thread_sleep.start()
                        while True:
                            result = self.speech_recognizer.recognize_once_async().get()
                            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                                print("")
                            if "wake up" in result.text.lower():
                                thread_wake = threading.Thread(target=playsound,args=(wake_mode,))
                                thread_wake.start()
                                break
                            else:
                                continue
                            
                    elif "play some" in result.text.lower() or "play" in result.text.lower() or "music" in result.text.lower():
                        await self.play_music(result.text.lower())   
                        
                    elif "switch" in result.text.lower() and "to" in result.text.lower() and "remote" in result.text.lower() and "access" in result.text.lower():
                        print("Switched to remote access , use you handheld device to access the device")
                        while True:
                            time.sleep(0.5)
                            await self.lock_screen_async()
                        
                    
                    elif "lock screen." == result.text.lower() or "screen." == result.text.lower() or "turn off." in result.text.lower():
                        tabs_handler.lockscreen()

                                
                    elif "shutdown" in result.text.lower():
                        self.speak_text("Goodbye boss! Have a nice day")
                        time.sleep(5)
                        exit()
                    
                    elif "iniitate" and "hand" and "gesture" in result.text.lower():
                        playsound(gesture_response)
                        thread = threading.Thread(target=self.handle_gesture)
                        thread.start()
                        thread.join()
                        
                    elif "dark search" in result.text.lower():
                        text = "initializing dark search"
                        self.speak_text(text)
                        thread = threading.Thread(target=self.dark_search,args=(result.text.lower(),))
                        thread.start()
                        thread.join()
                    
                    elif "initiate voice typing" in result.text.lower():
                        print ("reached")
                        playsound(voicetype_mode)
                        await self.handle_voice_type()
   

                    
                    elif "search" in result.text.lower():
                        prompt = result.text.lower().replace("generate", "").strip().replace(".", "").strip()
                        response = genai.generate_code(prompt)
                        self.speak_text(response)
                        
                    elif "initiate" in result.text.lower() and "proxy" in result.text.lower():
                        playsound(proxy_send)
                        wp.proxy()
                
                    
                   
                
        
        except Exception as e:
            logging.error(f"Error during speech recognition: {e}")
    
    
    async def lock_screen_async(self):
        # Asynchronously send a request to the specified Flask app's endpoint to lock the screen
        try:
            url = "http://13.235.16.223:8080/lock"
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                json_data = response.json()
                if json_data.get("lock_code") == "900":
                    tabs_handler.lockscreen()
            else:
                print("Failed to lock the screen - HTTP error")
        except Exception as e:
            print(f"Error sending lock request: {e}")

    
    def all_audio_initialise(self):
        tempaudiofile.cleanup()
        name = tempaudiofile.whatsapp_speech()
        return name
    
    async def handle_voice_type(self):
        stop_phrases = ["stop voice typing.", "stop voice.", "end voice typing.", "finish voice typing."]
        
        while True:
            try:
                result_voice_typing = self.speech_recognizer.recognize_once_async().get()

                if result_voice_typing.reason == speechsdk.ResultReason.RecognizedSpeech and result_voice_typing.text:
                    print("Recognized: {}".format(result_voice_typing.text))

                    # Check if the recognized text is in the stop phrases
                    if result_voice_typing.text.lower() in stop_phrases:
                        playsound(voicetype_mode_stop)
                        break
                    elif result_voice_typing.text.lower() == "pause voice typing":
                        playsound(voicetype_mode_pause)
                    elif result_voice_typing.text.lower() != "":
                        vc.typist(result_voice_typing.text.lower())
                    else:
                        continue

            except Exception as e:
                logging.error(f"Error during voice typing recognition: {e}")

    
    def speak_text(self, text):
        try:
            self.speech_synthesizer.speak_text_async(text).get()
        except Exception as e:
            logging.error(f"Error while speaking text: {e}")
    


    
    async def generate_audio_response(self, responses_dict, text, duration):
        responses_dict[text] = tempaudiofile.get_responses(text, duration)

    async def initialize_temporary_speeches(self):
        global whatsapp, luna, initial_response, gesture_response, proxy_send, ask_boss, app_close, sleep_mode, wake_mode, voicetype_mode,voicetype_mode_pause,voicetype_mode_stop

        responses_dict = {}

        # Define the responses and corresponding text and duration
        responses_info = [
            ("whatsapp starting", 1.2),
            ("yes i am listening", 1.2),
            ("hello i am luna , how can i help you", 1.2),
            ("initiating tactile control paradigm", 1.2),
            ("initiating proxy module", 1.2),
            ("closing the app", 1.2),
            ("boss do you want me to walk you through the day", 1.2),
            ("assistant is going sleep mode", 1.2),
            ("assistant is waking up", 1.2),
            ("initiating voice typing mode", 1.2),
            ("pausing voice typing mode", 1.2),
            ("stopping voice typing mode", 1.2),
        ]

        # Use asyncio.gather to asynchronously generate responses
        await asyncio.gather(
            *[self.generate_audio_response(responses_dict, text, duration) for text, duration in responses_info]
        )

        # Assign responses to global variables
        whatsapp, luna, initial_response, gesture_response, proxy_send, ask_boss, app_close, sleep_mode, wake_mode, voicetype_mode, voicetype_mode_pause,voicetype_mode_stop = (
            responses_dict["whatsapp starting"],
            responses_dict["yes i am listening"],
            responses_dict["hello i am luna , how can i help you"],
            responses_dict["initiating tactile control paradigm"],
            responses_dict["initiating proxy module"],
            responses_dict["boss do you want me to walk you through the day"],
            responses_dict["closing the app"],
            responses_dict["assistant is going sleep mode"],
            responses_dict["assistant is waking up"],
            responses_dict["initiating voice typing mode"],
            responses_dict["pausing voice typing mode"],
            responses_dict["stopping voice typing mode"],
        )
    
    def initialquestion(self):
        playsound(ask_boss)
        
        try:
            result = self.speech_recognizer.recognize_once_async().get()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Recognized: {}".format(result.text))
            if "yes" in result.text.lower():
                tb.get_today_classes()
            elif "no" in result.text.lower():
                print ("moving forward")
                
        except Exception as e:
            logging.error(f"Error during speech recognition: {e}")

    
    def get_data(self,param):
        conn = http.client.HTTPSConnection("youtube-music-api3.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Key': "65ddafd97fmsh1c40b1aad0c0e55p188efdjsn90dd67f4d815",
            'X-RapidAPI-Host': "youtube-music-api3.p.rapidapi.com"
        }
        print (param)
        
        new_param = param.strip().replace(" ", "%20")
        print (new_param)
        
        conn.request("GET", f"/search?q={new_param}&type=song", headers=headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")

        response_json = json.loads(data)

        video_ids = [item['videoId'] for item in response_json.get('result', [])[:19]]

        with open('video_ids.txt', 'w') as file:
            for video_id in video_ids:
                file.write(video_id + '\n')

        print("VideoIds saved to video_ids.txt")
    
    
    def dark_search(self,text):
        text = "initializing dark search"
        self.speak_text(text)
        result = text.replace("search", "").strip().replace(".", "").strip()
        darkmode.get_response(result)


        
      
    def play(self,query):
        print(query)
        self.get_data(query)
        time.sleep(3)
        video_ids = [line.strip() for line in open('video_ids.txt')]
        if video_ids:
            first_video_id = video_ids[0]
            driver = webdriver.Chrome()
            driver.get("https://www.youtube.com/watch?v=" + first_video_id)
            time.sleep(6)
            pyautogui.click(400,400)
            time.sleep(300)  # Adjust the duration as needed
        else:
            print("No video ids found")       
    
    def establish_preconnection(self):
        self.synthesizer = speechsdk.SpeechSynthesizer(self.speech_config, None)
        self.connection = speechsdk.Connection.from_speech_synthesizer(self.synthesizer)
        self.connection.open(True)
    
    def greet_user(self):
    
        hour = datetime.now().hour
        if (hour >= 6) and (hour < 12):
            self.speak_text(f"Good Morning")
        elif (hour >= 12) and (hour < 16):
          self.speak_text(f"Good afternoon")
        elif (hour >= 16) and (hour < 19):
            self.speak_text(f"Good Evening")
    





    # def handle_whatsapp(self):
    #     folder_path = "C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna\\test"
    #     playsound(whatsapp)
    #     self.speak_text("This part is very important! Say 'contact' and then the name of the person you want to send the text.")
        
    #     query = self.speech_recognizer.recognize_once_async().get()
    #     print(query.text.lower())

    #     if "contact" in query.text.lower():
    #         name = query.text.lower().replace("contact", "").strip().replace(".", "").strip()
    #         if name is not None:
    #             whatsapp.send_files_in_folder(folder_path, name)
        
    def luna_response_check(self):
        playsound(luna)
        
    
    async def play_music(self,text):
        name = text.replace("play", "").replace("play some", "").replace("music", "").strip().replace(".", "").strip().replace("please","").strip()
        thread = threading.Thread(target=ms.luna_playback,args=(name,))
        thread.start()
        
        
    async def handle_apps_open_async(self, app):    
        name = app.replace("open", "").strip().replace(".", "").strip()
        # char_iterator = iter(text)
        # self.stream.feed(char_iterator)
        # self.stream.play_async()
        if name is not None:
                ut.open_app(name)
                
    
    async def handle_apps_close_async(self, app):
        self.establish_preconnection()
        name = app.replace("close", "").strip().replace(".", "").strip().replace("please","").replace("45","spotify")
        # thread1 = threading.Thread(target=playsound, args=(app_close,))
        # thread1.start()
        # playsound(app_close)
        # text = f"closing {name}"
        # char_iterator = iter(text)
        # self.stream.feed(char_iterator)
        # self.stream.play_async()
        if name is not None:
                thread2 = threading.Thread(target=ut.close_app, args=(name,))
                thread2.start()
                # ut.close_app(name)
    
    def handle_gesture(self):
        ut.gesture_mode()
    
    
    async def continuous_recognition(self):
        try:
            playsound(initial_response)
            print("Speak into your microphone. Press 'Ctrl+C' to exit.")

            await asyncio.gather(
                self.recognize_speech(),
            )

        except KeyboardInterrupt:
            print("Recognition loop terminated.")
            sys.exit("exiting...")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    tempaudiofile.cleanup()
    recognition = ContinuousRecognition()
    # Use asyncio.run to run the asynchronous initialization
    asyncio.run(recognition.initialize_temporary_speeches())
    recognition.greet_user()
    recognition.initialquestion()

    # Create a new event loop and run the continuous_recognition coroutine
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(recognition.continuous_recognition())
    except KeyboardInterrupt:
        print("Recognition loop terminated.")
        sys.exit("exiting...")

