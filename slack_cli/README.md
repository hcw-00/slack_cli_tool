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