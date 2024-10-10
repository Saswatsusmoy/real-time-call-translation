import os
import azure.cognitiveservices.speech as speechsdk

speech_key = '3fcc10f1c7fc4c82af2cb58912dbbe9f'
service_region = 'centralindia'

def translate_speech_to_speech():
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key, region=service_region)
    
    translation_config.speech_recognition_language = 'hi-IN'
    translation_config.add_target_language('en')
    
    audio_config = speechsdk.audio.AudioConfig(filename="C:/Users/saswa/OneDrive/Desktop/Call_translation/sample4.wav")
    translator = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config)

    result = translator.recognize_once()
    
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print(f"Recognized: {result.text}")
        
        for language, translation in result.translations.items():
            print(f"Translated into '{language}': {translation}")
            
            voices = {
                'en': 'en-US-JennyNeural'
            }
            speech_config = speechsdk.SpeechConfig(
                subscription=speech_key, region=service_region)
            speech_config.speech_synthesis_voice_name = voices.get(language)
            
            audio_config = speechsdk.audio.AudioOutputConfig(
                filename=f"{language}-translation.wav")
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config, audio_config=audio_config)
            speech_synthesizer.speak_text_async(translation).get()
    
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

translate_speech_to_speech()
