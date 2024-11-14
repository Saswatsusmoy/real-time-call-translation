import tkinter as tk
import azure.cognitiveservices.speech as speechsdk
import threading

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Translator")
        self.root.geometry("400x300")
        
        self.is_listening = False
        self.speech_key = '3fcc10f1c7fc4c82af2cb58912dbbe9f'
        self.service_region = 'centralindia'
        
        # Create and configure the speak button
        self.speak_button = tk.Button(
            root, 
            text="Speak", 
            command=self.toggle_listening,
            width=20,
            height=2,
            font=("Arial", 14)
        )
        self.speak_button.pack(pady=20)
        
        # Create text display area
        self.text_area = tk.Text(root, height=10, width=40)
        self.text_area.pack(pady=20)
        
        # Initialize speech synthesizer
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, 
            region=self.service_region
        )
        speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    def toggle_listening(self):
        if not self.is_listening:
            self.speak_button.config(text="Stop Listening", bg="red")
            self.is_listening = True
            # Start listening in a separate thread
            threading.Thread(target=self.start_translation, daemon=True).start()
        else:
            self.speak_button.config(text="Speak", bg="SystemButtonFace")
            self.is_listening = False

    def speak_translation(self, text):
        try:
            self.speech_synthesizer.speak_text_async(text).get()
        except Exception as ex:
            self.update_text_area(f"Speech synthesis error: {str(ex)}\n")

    def start_translation(self):
        translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=self.speech_key, 
            region=self.service_region
        )
        
        translation_config.speech_recognition_language = 'hi-IN'
        translation_config.add_target_language('en')
        
        # Configure for microphone input
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        translator = speechsdk.translation.TranslationRecognizer(
            translation_config=translation_config, 
            audio_config=audio_config
        )

        def handle_result(evt):
            if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
                recognized_text = f"Recognized: {evt.result.text}\n"
                self.update_text_area(recognized_text)
                
                for language, translation in evt.result.translations.items():
                    translated_text = f"Translated to {language}: {translation}\n"
                    self.update_text_area(translated_text)
                    
                    # Speak the translated text in a separate thread
                    threading.Thread(
                        target=self.speak_translation,
                        args=(translation,),
                        daemon=True
                    ).start()

        def handle_canceled(evt):
            if evt.cancellation_details.reason == speechsdk.CancellationReason.Error:
                error_text = f"Error: {evt.cancellation_details.error_details}\n"
                self.update_text_area(error_text)

        translator.recognized.connect(handle_result)
        translator.canceled.connect(handle_canceled)
        
        translator.start_continuous_recognition()
        while self.is_listening:
            pass
        translator.stop_continuous_recognition()

    def update_text_area(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
