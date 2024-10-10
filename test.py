import os
import threading
import tkinter as tk
from tkinter import filedialog
import azure.cognitiveservices.speech as speechsdk

speech_key = '3fcc10f1c7fc4c82af2cb58912dbbe9f'
service_region = 'centralindia'

def translate_speech_to_speech(input_file):
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key, region=service_region)
    
    translation_config.speech_recognition_language = 'en-US'
    translation_config.add_target_language('or')
    
    audio_config = speechsdk.audio.AudioConfig(filename=input_file)
    translator = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config)

    voices = {
        'or': 'or-IN-BhagyaNeural'
    }
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = voices.get('or')
    
    audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)

    result = translator.recognize_once()
    
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print(f"Recognized: {result.text}")
        
        for language, translation in result.translations.items():
            print(f"Translated into '{language}': {translation}")
            speech_synthesizer.speak_text_async(translation).get()
            pygame.mixer.music.load("output.wav")
            pygame.mixer.music.play()
    
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if file_path:
        threading.Thread(target=translate_speech_to_speech, args=(file_path,)).start()

pygame.mixer.init()

root = tk.Tk()
root.title("Speech Translation")

upload_button = tk.Button(root, text="Upload Audio", command=upload_file)
upload_button.pack(pady=20)

root.mainloop()
