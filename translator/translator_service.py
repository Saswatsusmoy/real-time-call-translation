import requests
from urllib.parse import quote
from config import AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION

def translate_text(text: str, target_language: str = 'en') -> str:
    """
    Translates the given text to the target language using Azure Translator.

    Args:
        text (str): Text to translate.
        target_language (str): Language code to translate the text into.

    Returns:
        str: Translated text.
    """
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate?api-version=3.0'
    params = f'&to={quote(target_language)}'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_TRANSLATOR_REGION,
        'Content-Type': 'application/json'
    }

    body = [{
        'text': text
    }]

    response = requests.post(constructed_url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()

    return result[0]['translations'][0]['text']