import io
import os
import tempfile
import azure.cognitiveservices.speech as speechsdk
from playsound import playsound
from pydub import AudioSegment
import random
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription="", region="eastus")
audio_config = speechsdk.audio.PullAudioOutputStream()  # Disable audio output

speech_config.speech_synthesis_voice_name = 'en-US-AmberNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# this is the whatsapp speech block

# whatsapp_text = "Whatsapp module is beginning sequence"
# whatsapp = speech_synthesizer.speak_text_async(whatsapp_text).get()

# # this is the luna speech block

# luna_text = ["Yes, I can hear you", "I am listening", "I am here", "Yes, I am here", "Yes, I am listening", "You speak too loudly"]
# luna_speech = random.choice(luna_text)
# luna = speech_synthesizer.speak_text_async(luna_speech).get()

# # the first greeting message

# initial_text = "Hello i am luna, A virtual assistant. How can I help you?"
# initial = speech_synthesizer.speak_text_async(initial_text).get()

# # the gesture block

# gesture_text = "initiating tactile control paradigm"
# gesture = speech_synthesizer.speak_text_async(gesture_text).get()


# def whatsapp_speech():
#     whatsapp_data = None  # Initialize the variable
#     if whatsapp.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         whatsapp_data = whatsapp.audio_data
    
#     if whatsapp_data is not None:
#         whatsapp_buffer = io.BytesIO(whatsapp_data)
#         temp_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir="C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna").name
#         with open(temp_file_path, "wb") as temp_file:
#             temp_file.write(whatsapp_buffer.getvalue())
#         return temp_file_path
#     else:
#         # Handle the case where whatsapp_data is not available
#         print("Error: Synthesizing audio not completed.")
#         return None

# def luna_speech():
#     luna_data = None  # Initialize the variable
#     if luna.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         luna_data = luna.audio_data
    
#     if luna_data is not None:
#         luna_buffer = io.BytesIO(luna_data)
#         temp_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir="C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna").name
#         with open(temp_file_path, "wb") as temp_file:
#             temp_file.write(luna_buffer.getvalue())
#         return temp_file_path
#     else:
#         # Handle the case where whatsapp_data is not available
#         print("Error: Synthesizing audio not completed.")
#         return None
    
# def initial_response():
#     initial_data = None  # Initialize the variable
#     if initial.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         initial_data = initial.audio_data
    
#     if initial_data is not None:
#         luna_buffer = io.BytesIO(initial_data)
#         temp_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir="C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna").name
#         with open(temp_file_path, "wb") as temp_file:
#             temp_file.write(luna_buffer.getvalue())
#         return temp_file_path
#     else:
#         # Handle the case where initial_data is not available
#         print("Error: Synthesizing audio not completed.")
#         return None
    
    
# def gesture_response():
#     gesture_data = None  # Initialize the variable
#     if gesture.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         gesture_data = gesture.audio_data
    
#     if gesture_data is not None:
#         gesture_buffer = io.BytesIO(gesture_data)
#         temp_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir="C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna").name
#         with open(temp_file_path, "wb") as temp_file:
#             temp_file.write(gesture_buffer.getvalue())
#         return temp_file_path
#     else:
#         # Handle the case where gesture_data is not available
#         print("Error: Synthesizing audio not completed.")
#         return None

def change_speed(file_path, speed):
    audio = AudioSegment.from_file(file_path, format="wav")

    if speed == 0:
        # If speed is zero, export the original audio without modification
        audio.export(file_path, format="wav")
    else:
        modified_audio = audio.speedup(playback_speed=speed)
        modified_audio.export(file_path, format="wav")


def module_function(response):
    response_data = None  # Initialize the variable
    if response.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        response_data = response.audio_data
    
    if response_data is not None:
        response_buffer = io.BytesIO(response_data)
        temp_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir="C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna").name
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(response_buffer.getvalue())
        return temp_file_path
    else:
        # Handle the case where gesture_data is not available
        print("Error: Synthesizing audio not completed.")
        return None
    
    
    
def cleanup():
    for file_name in os.listdir("C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna"):
        if file_name.endswith(".wav"):
            file_path = os.path.join("C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna", file_name)
            os.remove(file_path)


def get_responses(text,speedlim):
    speak_text = speech_synthesizer.speak_text_async(text).get()
    var = module_function(speak_text)
    change_speed(var, speed=speedlim)
    return var
    
    

def main():
    
    cleanup()
    name = get_responses("hi how are you",1.2)

    # # Change the speed of the audio file
    # change_speed(name, speed=0)  # Adjust the speed factor as needed

    # # Play the modified audio file
    # playsound(name)
    playsound(name)


if __name__ == "__main__":
    main()
