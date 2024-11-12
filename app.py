from flask import Flask, request, jsonify
import speech_recognition as sr
from translate import Translator

app = Flask(__name__)

# Ruta para traducción
@app.route('/translate', methods=['POST'])
def translate():
    # Captura el JSON del cliente
    data = request.get_json()

    # Verifica que se envió el texto y el idioma de destino
    if 'transcript' not in data or 'language' not in data:
        return jsonify({'error': 'Faltan datos en la solicitud'}), 400

    transcript = data['transcript']
    language = data['language']

    # Traduce el texto usando Translator
    translator = Translator(to_lang=language)
    try:
        translated_text = translator.translate(transcript)
        return jsonify({'translated_text': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
