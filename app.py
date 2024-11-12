import os
from flask import Flask, request, jsonify
import speech_recognition as sr
from googletrans import Translator
from werkzeug.utils import secure_filename

# Configuración
app = Flask(__name__)

# Ruta para el procesamiento del audio y traducción
@app.route('/translate', methods=['POST'])
def translate():
    # Verificar si el archivo 'audio' está presente en la solicitud
    if 'audio' not in request.files:
        return jsonify({"error": "No se encontró el archivo 'audio' en la solicitud"}), 400
    
    audio_file = request.files['audio']
    
    # Verificar si el archivo tiene un nombre
    if audio_file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400

    # Guardar temporalmente el archivo
    filename = secure_filename(audio_file.filename)
    audio_path = os.path.join('uploads', filename)
    audio_file.save(audio_path)

    # Usar SpeechRecognition para transcribir el audio
    recognizer = sr.Recognizer()
    
    # Abrir el archivo de audio y convertirlo a texto
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data, language='es-ES')  # Transcribir a español
    except Exception as e:
        return jsonify({"error": f"No se pudo transcribir el audio: {str(e)}"}), 400

    # Traducir el texto
    translator = Translator()
    target_language = request.form.get('language', 'en')  # Idioma de destino, por defecto inglés
    translation = translator.translate(transcript, dest=target_language)

    # Devolver la transcripción y la traducción
    return jsonify({
        "transcript": transcript,
        "translated_text": translation.text
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
