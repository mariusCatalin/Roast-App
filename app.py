import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
from PIL import Image
import io
import base64

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')


def get_roast(image_data):
    try:
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": image_data
            },
        ]

        prompt_parts = [
            "Esti o persoana care face standup comedy si ceea ce trebuie sa faci e sa faci un roast spicy pentru aceasta poza. Fi cat de dur poti. Raspunsul trebuie sa fie in limba romana.",
            image_parts[0]
        ]

        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"Error generating roast: {str(e)}"


@app.route('/roast', methods=['POST'])
def roast_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        image_data = image_file.read()

        roast_text = get_roast(image_data)

        return jsonify({'roast': roast_text}), 200
    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500
    
@app.route('/')
def index():
    return send_file("index.html")

if __name__ == '__main__':
    app.run(debug=True)
