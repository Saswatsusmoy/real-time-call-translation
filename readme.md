# Audio Translator

## Overview

Audio Translator is a Python-based application that leverages Azure Cognitive Services to transcribe audio files and translate the transcribed text into a specified target language. This project utilizes Azure Speech-to-Text for audio transcription and Azure Translator for text translation.

## Features

- Transcribe audio files (WAV and MP3 formats supported)
- Translate transcribed text to a specified target language
- Simple command-line interface
- Error handling for various scenarios
- Extensible architecture for future enhancements

## File Structure

- `requirements.txt`: Lists all Python dependencies
- `config.py`: Contains Azure service credentials and settings
- `translator/__init__.py`: Initializer for the translator package
- `translator/audio_processor.py`: Handles audio transcription using Azure Speech-to-Text
- `translator/translator_service.py`: Manages text translation using Azure Translator
- `main.py`: Main script to execute the audio translation workflow
- `test.py`: A GUI-based test script for speech-to-speech translation

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/audio-translator.git
   cd audio-translator
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Azure Credentials:
   - Open `config.py`
   - Replace the placeholder values with your actual Azure credentials:
     ```python
     AZURE_SPEECH_KEY = 'YOUR_AZURE_SPEECH_KEY'
     AZURE_SPEECH_REGION = 'YOUR_AZURE_SPEECH_REGION'
     AZURE_TRANSLATOR_KEY = 'YOUR_AZURE_TRANSLATOR_KEY'
     AZURE_TRANSLATOR_REGION = 'YOUR_AZURE_TRANSLATOR_REGION'
     ```

## Usage

### Command-line Interface

Run the main script with the path to your audio file and specify the target language if desired:

```
python main.py path/to/audiofile.wav --target_lang es
```

Arguments:
- `path/to/audiofile.wav`: Replace with the path to your audio file (WAV or MP3)
- `--target_lang es`: (Optional) Replace `es` with your desired target language code (e.g., `en` for English, `fr` for French)

### GUI Interface (Test Script)

The `test.py` script provides a simple GUI for speech-to-speech translation:

1. Run the script:
   ```bash
   python test.py


Arguments:
- `path/to/audiofile.wav`: Replace with the path to your audio file (WAV or MP3)
- `--target_lang es`: (Optional) Replace `es` with your desired target language code (e.g., `en` for English, `fr` for French)

### GUI Interface (Test Script)

The `test.py` script provides a simple GUI for speech-to-speech translation:

1. Run the script:
   ```
   python test.py
   ```
2. Click the "Upload Audio" button to select a WAV file.
3. The script will transcribe the audio, translate it to Odia, and generate an output audio file.

## Error Handling

The application includes error handling for various scenarios:
- Unrecognized speech in the audio file
- Cancellation of the transcription process
- HTTP errors from the translation service

Errors will be printed to the console with descriptive messages.

## Extensibility

The project structure allows for easy addition of new features:
- Support for additional audio formats
- Integration of multiple translation services
- Development of a more comprehensive user interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

This project uses Azure Cognitive Services, including Azure Speech Service and Azure Translator. Please ensure you comply with Microsoft's terms of service and pricing when using these services.
