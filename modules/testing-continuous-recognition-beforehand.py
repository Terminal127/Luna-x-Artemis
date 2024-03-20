import tkinter as tk
import azure.cognitiveservices.speech as speechsdk

class ContinuousRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Continuous Speech Recognition")
        self.continuous_listening_started = False
        self.reco = None
        self.audio_input = None
        self.button_text = tk.StringVar()
        self.button_text.set("Start Continuous Recognition")
        self.current_text = ""

        self.create_widgets()

    def create_widgets(self):
        self.text_box = tk.Text(self.root, height=2, width=50)
        self.text_box.pack(pady=10)

        self.recognize_button = tk.Button(self.root, textvariable=self.button_text, command=self.toggle_recognition)
        self.recognize_button.pack()

    def toggle_recognition(self):
        if self.continuous_listening_started:
            if self.reco is not None:
                self.reco.stop_continuous_recognition_async()
                self.root.after(100, self.on_continuous_recognition_stopped)
        else:
            self.clear_text_box()

            self.audio_input = speechsdk.audio.AudioConfig(use_default_microphone=True)
            self.reco = speechsdk.SpeechRecognizer(speech_config=self.get_speech_config(), audio_config=self.audio_input)

            self.reco.recognizing.connect(lambda evt: self.on_intermediate_result(evt.result.text))
            self.reco.recognized.connect(lambda evt: self.on_final_result(evt.result.text))

            self.reco.start_continuous_recognition_async()

            self.continuous_listening_started = True
            self.button_text.set("Stop Continuous Recognition")

    def on_intermediate_result(self, text):
        print("Intermediate result received:", text)
        # Append the intermediate result to the same line
        self.update_text_box(text + " ")

    def on_final_result(self, text):
        print("Final result received:", text)
        # Append the final result to the same line with a new line
        self.update_text_box(text + "\n")

    def on_continuous_recognition_stopped(self):
        print("Continuous recognition stopped.")
        self.continuous_listening_started = False
        self.button_text.set("Start Continuous Recognition")

    def clear_text_box(self):
        self.text_box.delete(1.0, tk.END)
        self.current_text = ""

    def update_text_box(self, new_text):
        # Remove the previous text and append the new text to the same line
        self.text_box.delete(1.0, tk.END)
        self.current_text += new_text
        self.text_box.insert(tk.END, self.current_text)

    def get_speech_config(self):
        speech_key = ""
        service_region = "eastus"

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        return speech_config

if __name__ == "__main__":
    root = tk.Tk()
    app = ContinuousRecognitionApp(root)
    root.mainloop()
