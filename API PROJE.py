from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio_file']

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({'text': text}), 200
        except sr.UnknownValueError:
            return jsonify({'error': 'Speech not recognized'}), 400
        except sr.RequestError as e:
            return jsonify({'error': 'Google Speech service error: {}'.format(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
