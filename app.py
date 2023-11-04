from flask import Flask, render_template,request,jsonify
from googletrans import Translator
from gtts import gTTS
import base64
import tempfile
import speech_recognition as sr

app = Flask(__name__)

# Create a recognizer and a microphone instance
recognizer = sr.Recognizer()

translator = Translator()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/text_to_text',methods=["POST","GET"])
def text_to_text():
    if request.method == 'POST':
        text = request.form['text']
        target_lang = request.form['target_lang']
        
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        
        return render_template('text_to_text.html', translation=translation.text)
    return render_template('text_to_text.html')

@app.route('/speech_to_speech')
def speech_to_speech():
    return render_template('speech_to_speech.html')


@app.route('/translate', methods=['POST'])
def translate_text():
    text = request.form['text']
    target_lang = request.form['target_lang']

    try:
        translated_text = translator.translate(text, dest=target_lang).text
        tts = gTTS(text=translated_text, lang=target_lang)

        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
            tts.save(temp_audio_file.name)
            temp_audio_file.seek(0)
            audio_data = temp_audio_file.read()

        # Convert the binary audio data to a Base64 string
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        return jsonify({'translated_text': translated_text, 'audio_data': audio_base64})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
