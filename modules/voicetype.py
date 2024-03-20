import pyautogui
import pygetwindow as gw
import azure.cognitiveservices.speech as speechsdk
import asyncio

speech_config = speechsdk.SpeechConfig(subscription="0b056629cf414956afb50b976d4c5487", region="eastus")
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_config.speech_synthesis_voice_name = 'en-US-AmberNeural'
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def bring_notepad_to_front():
    notepad_window = gw.getWindowsWithTitle("Notepad")

    if notepad_window:
        notepad_window[0].activate()
    else:
        print("Notepad is not open. Opening Notepad.")
        pyautogui.hotkey('win', 'r')
        pyautogui.write('notepad')
        pyautogui.press('enter')

def typist(text):
    bring_notepad_to_front()
    pyautogui.typewrite(text, interval=0.01)  # Adjust interval as needed
    pyautogui.press('enter')

def handle_voice_typing_async():
    bring_notepad_to_front()

    while True:
        try:
            result_voice_typing = speech_recognizer.recognize_once_async().get()

            if result_voice_typing.reason == speechsdk.ResultReason.RecognizedSpeech and result_voice_typing.text:
                print("Recognized: {}".format(result_voice_typing.text))

                if "stop voice typing" in result_voice_typing.text.lower():
                    break
                elif result_voice_typing.text.lower() == "pause voice typing.":
                    print("Paused")
                    # Add a pause to avoid immediate recognition
                elif result_voice_typing.text.lower() != "":
                    typist(result_voice_typing.text.lower())
                else:
                    continue

        except Exception as e:
            print(f"Error during voice typing recognition: {e}")

if __name__ == "__main__":
    handle_voice_typing_async()
