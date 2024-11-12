from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate():
    try:
        # Recibe los datos JSON desde la solicitud
        data = request.get_json()
        
        # Extrae el texto a traducir y el idioma de destino
        transcript = data.get('transcript')
        target_language = data.get('language')
        
        if not transcript or not target_language:
            return jsonify({"error": "Faltan datos en la solicitud."}), 400

        # Realiza la traducción
        translation = translator.translate(transcript, dest=target_language)
        
        # Devuelve la traducción en formato JSON
        return jsonify({
            'transcript': transcript,
            'translated_text': translation.text
        })
    
    except Exception as e:
        # En caso de error, muestra un mensaje descriptivo en JSON
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
