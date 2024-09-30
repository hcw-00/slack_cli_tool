import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, Response, jsonify
from dotenv import load_dotenv
# import jsonify

load_dotenv()

app = Flask(__name__)

# Your bot token (from OAuth & Permissions)
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# Example automation to send a message in response to a specific keyword
def send_message(channel, text):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json

    # Check if the request is a URL verification challenge from Slack
    if data.get('type') == 'url_verification':
        # Respond with the challenge token in plain text
        return data.get('challenge'), 200
    
    # Normal event handling code for other events (e.g., messages)
    if 'event' in data:
        event = data['event']
        
        # Example automation: Respond if the message contains "hello"
        if event.get('type') == 'message' and 'hello' in event.get('text', ''):
            send_message(event['channel'], "Hi there! How can I help you?")
        
        # Handle other event types here as needed
        print("Event received:", event)

    return jsonify({"status": "ok"}), 200

def send_message(channel, text):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

if __name__ == "__main__":
    app.run(port=3000, debug=True)
