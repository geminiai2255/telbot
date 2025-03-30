import os
import json
import requests
from flask import Flask, request

# Flask app to handle the webhook
app = Flask(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token from @BotFather
bot_token = '8130860956:AAEeuIM-BU58IXELUQIrfP6vxF5_moQ5brw'

# Replace with your actual Vercel URL
vercel_url = 'https://telbot-three.vercel.app' 

# Set webhook for Telegram Bot
def set_webhook():
    webhook_url = f"https://api.telegram.org/bot8130860956:AAEeuIM-BU58IXELUQIrfP6vxF5_moQ5brw/setWebhook?url=https://telbot-three.vercel.app/webhook"
    response = requests.get(webhook_url)
    print(response.json())

# This will be called when the bot receives a message
@app.route('/webhook', methods=['POST'])
def webhook():
    # Parse the incoming data from Telegram
    update = request.get_json()

    chat_id = update['message']['chat']['id']
    text = update['message']['text']

    # Respond to the received message
    send_message(chat_id, f"Received your message: {text}")

    return "OK"

# Send a message to a chat
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text
    }
    requests.get(url, params=params)

if __name__ == '__main__':
    # Set the webhook when the app starts
    set_webhook()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
