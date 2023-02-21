import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import translate_v2 as translate

def transcribe_and_translate(audio_file, target_language):
    # Instantiates a client
    speech_client = speech.SpeechClient()

    # Loads the audio file into memory
    with io.open(audio_file, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    # Specifies the language of the audio
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US')

    # Detects speech in the audio file
    response = speech_client.recognize(config, audio)

    # Extracts the text from the response
    transcript = response.results[0].alternatives[0].transcript

    # Instantiates a client
    translate_client = translate.Client()

    # Translates the text into the target language
    translation = translate_client.translate(
        transcript, target_language=target_language)

    # Converts the translated text into speech
    tts_client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=translation['translatedText'])
    voice = texttospeech.VoiceSelectionParams(
        language_code=target_language,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)

    # Saves the synthesized speech to a file
    with open('output.wav', 'wb') as out:
        out.write(response.audio_content)