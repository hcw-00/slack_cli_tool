# Slack CLI Tool

This is a command-line interface (CLI) tool for interacting with Slack. It allows you to upload images, post messages, and retrieve channel history directly from your terminal.

## Installation

You can install this tool using pip:

```
pip install git+https://github.com/yourusername/slack-cli-tool.git
```

## Setup

1. Clone this repository or download the files (`slack.py`, `slack`, and `slack.bat`) to your local machine.

2. Install the required Python packages:
   ```bash
   pip install requests python-dotenv
   ```

3. Create a `.env` file in the same directory as the scripts with the following content:
   ```bash
   SLACK_TOKEN=your_slack_token_here
   CHANNEL_ID=your_channel_id_here
   ```
   Replace `your_slack_token_here` and `your_channel_id_here` with your actual Slack token and channel ID.

4. Add the directory containing these files to your system's PATH.

## Usage

The tool supports three main commands: `upload`, `post`, and `history`.

### Upload an image
slack upload path/to/image.jpg
### Post a message
slack post "Your message here"
### Get channel history

You can also specify the number of messages to retrieve:

slack history --limit 50

## Platform Compatibility

This tool is designed to work on both Unix-based systems (macOS, Linux) and Windows.

## Note

Make sure you have the necessary permissions in your Slack workspace to perform these actions.

## Slack Event Handler

A new file `slack_event_handler.py` has been added to handle Slack events and respond to messages.

### Usage

1. Ensure you have the necessary environment variable set for your bot token:
   ```bash
   SLACK_BOT_TOKEN=your_slack_bot_token_here
   ```

2. Start the Flask application:
   ```bash
   python slack_event_handler.py
   ```

3. The application listens for events from Slack at the `/slack/events` endpoint. It responds to messages containing "hello" with a friendly greeting.

4. **Make sure your Slack app is configured to send events to your server's URL.** To receive events from Slack, your server must be publicly accessible. You can use services like ngrok(or cloudflare, etc...) to expose your local server to the internet.

5. Make sure your Slack app is configured to send events to your server's URL.

## Additional Notes

- Ensure you have Flask and slack_sdk installed:
   ```bash
   pip install Flask slack-sdk
   ```