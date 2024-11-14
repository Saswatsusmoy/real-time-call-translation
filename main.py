import os
import azure.cognitiveservices.speech as speechsdk

speech_key = '3fcc10f1c7fc4c82af2cb58912dbbe9f'
service_region = 'centralindia'

def translate_speech_to_speech():
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key, region=service_region)
    
    translation_config.speech_recognition_language = 'hi-IN'
    translation_config.add_target_language('en')
    
    audio_config = speechsdk.audio.AudioConfig(filename="C:/Users/saswa/OneDrive/Desktop/Call_translation/sample3.wav")
    translator = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config)

    done = False

    def handle_result(evt):
        if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
            print(f"Recognized: {evt.result.text}")
            
            for language, translation in evt.result.translations.items():
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

    def handle_canceled(evt):
        print(f"Speech Recognition canceled: {evt.cancellation_details.reason}")
        if evt.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {evt.cancellation_details.error_details}")
        nonlocal done
        done = True

    translator.recognized.connect(handle_result)
    translator.canceled.connect(handle_canceled)

    translator.start_continuous_recognition()
    while not done:
        pass
    translator.stop_continuous_recognition()

translate_speech_to_speech()
