import azure.cognitiveservices.speech as speechsdk
from config import AZURE_SPEECH_KEY, AZURE_SPEECH_REGION
import os
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_file_path: str) -> str:
    """
    Converts an MP3 file to WAV format.

    Args:
        mp3_file_path (str): Path to the MP3 file.

    Returns:
        str: Path to the converted WAV file.
    """
    wav_file_path = os.path.splitext(mp3_file_path)[0] + '.wav'
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format='wav')
    return wav_file_path

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes the given audio file to text using Azure Speech-to-Text.

    Args:
        audio_file_path (str): Path to the audio file.

    Returns:
        str: Transcribed text.
    """
    if not audio_file_path.lower().endswith('.wav'):
        if audio_file_path.lower().endswith('.mp3'):
            audio_file_path = convert_mp3_to_wav(audio_file_path)
        else:
            raise ValueError("Unsupported audio format. Please provide a WAV or MP3 file.")

    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    audio_input = speechsdk.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        raise ValueError("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise RuntimeError(f"Speech Recognition canceled: {cancellation_details.reason}")