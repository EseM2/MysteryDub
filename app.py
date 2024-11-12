import os
from flask import Flask, render_template, request, jsonify
import openai
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from pydub.playback import play

# Configura tu API de OpenAI
openai.api_key = "TU_API_KEY"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    audio_file = request.files['audio']
    language_to = request.form['language_to']

    # Guarda el archivo de audio
    audio_path = "audio_input.wav"
    audio_file.save(audio_path)

    # Usa SpeechRecognition y Whisper para detectar y transcribir el idioma
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        # Usa Whisper para transcripción de voz y detección de idioma
        result = openai.Audio.transcribe("whisper-1", audio)
        detected_text = result['text']
        detected_language = result['language']

        # Traduce el texto al idioma deseado usando deep-translator
        translated_text = GoogleTranslator(source=detected_language, target=language_to).translate(detected_text)

        # Devuelve el texto traducido como JSON
        return jsonify({'text': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
