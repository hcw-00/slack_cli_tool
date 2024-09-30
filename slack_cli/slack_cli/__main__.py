#!/usr/bin/env python3

import argparse
import requests
import os
from dotenv import load_dotenv
import json
import sys
from urllib.parse import urlparse
from pathlib import Path

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# API endpoints
UPLOAD_URL = "https://slack.com/api/files.getUploadURLExternal"
COMPLETE_UPLOAD_URL = "https://slack.com/api/files.completeUploadExternal"
POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
SLACK_HISTORY_URL = "https://slack.com/api/conversations.history"
FILES_LIST_URL = "https://slack.com/api/files.list"
FILE_INFO_URL = "https://slack.com/api/files.info"

# Image upload functions
def get_file_size(file_path):
    """Returns the size of the image file in bytes"""
    return os.path.getsize(file_path)

def get_upload_url(token, filename, file_size):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "channels": CHANNEL_ID,
        "filename": filename,
        "length": file_size
    }
    response = requests.post(UPLOAD_URL, headers=headers, data=data)
    if response.status_code == 200:
        result = response.json()
        if result['ok']:
            return result['upload_url'], result['file_id']
        else:
            print(f"Error: {result['error']}")
            return None, None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None, None

def upload_image_to_url(upload_url, file_path):
    with open(file_path, "rb") as binary_data:
        files = {"file": binary_data}
        response = requests.post(upload_url, files=files)
        print("Upload response status:", response.status_code)
        print("Upload response text:", response.text)
        if response.status_code == 200:
            print("Image uploaded successfully!")
            return True
        else:
            print(f"HTTP Error: {response.status_code}")
            return False

def complete_upload(token, file_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "files": [{"id": file_id}],
        "channel_id": CHANNEL_ID
    }
    print(data)
    response = requests.post(COMPLETE_UPLOAD_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result['ok']:
            print("File upload completed successfully!")
        else:
            print(f"Error: {result['error']}")
    else:
        print(f"HTTP Error: {response.status_code}")

def upload_image(image_file_path):
    file_size = get_file_size(image_file_path)
    upload_url, file_id = get_upload_url(SLACK_TOKEN, os.path.basename(image_file_path), file_size)
    
    if upload_url and file_id:
        if upload_image_to_url(upload_url, image_file_path):
            complete_upload(SLACK_TOKEN, file_id)

# Message posting function
def post_message(text):
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "channel": CHANNEL_ID,
        "text": text
    }
    
    response = requests.post(POST_MESSAGE_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result['ok']:
            print("Message posted successfully!")
        else:
            print(f"Error: {result['error']}")
    else:
        print(f"HTTP Error: {response.status_code}")

# Channel history function
def get_channel_messages(limit=100):
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    
    params = {
        "channel": CHANNEL_ID,
        "limit": limit
    }
    
    response = requests.get(SLACK_HISTORY_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        messages = response.json()
        if messages['ok']:
            return messages['messages']
        else:
            print(f"Error: {messages['error']}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None

def get_file(file_id, output_dir="."):
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    
    # Get file info
    params = {
        "file": file_id
    }
    response = requests.get(FILE_INFO_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        file_info = response.json()
        if file_info['ok']:
            file_url = file_info['file']['url_private_download']
            file_name = file_info['file']['name']
            
            # Download file
            download_response = requests.get(file_url, headers=headers)
            if download_response.status_code == 200:
                output_path = Path(output_dir) / file_name
                with open(output_path, 'wb') as f:
                    f.write(download_response.content)
                print(f"File downloaded successfully: {output_path}")
            else:
                print(f"Error downloading file: HTTP {download_response.status_code}")
        else:
            print(f"Error: {file_info['error']}")
    else:
        print(f"HTTP Error: {response.status_code}")

def list_files(limit=10):
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    
    params = {
        "channel": CHANNEL_ID,
        "limit": limit
    }
    
    response = requests.get(FILES_LIST_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        files_info = response.json()
        if files_info['ok']:
            return files_info['files']
        else:
            error_message = files_info.get('error', 'Unknown error')
            if error_message == 'missing_scope':
                print("Error: The Slack token doesn't have the necessary permissions.")
                print("Please add the 'files:read' scope to your Slack app and update the token.")
                print("Visit https://api.slack.com/apps to configure your app.")
            else:
                print(f"Error: {error_message}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Slack Chat CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Upload image command
    upload_parser = subparsers.add_parser("upload", help="Upload an image to Slack")
    upload_parser.add_argument("image_path", help="Path to the image file")

    # Post message command
    post_parser = subparsers.add_parser("post", help="Post a message to Slack")
    post_parser.add_argument("message", help="Message to post")

    # Get channel messages command
    history_parser = subparsers.add_parser("history", help="Get channel message history")
    history_parser.add_argument("--limit", type=int, default=100, help="Number of messages to retrieve (default: 100)")

    # Get file command
    get_parser = subparsers.add_parser("get", help="Get a file from Slack")
    get_parser.add_argument("file_id", help="ID of the file to retrieve")
    get_parser.add_argument("--output", default=".", help="Output directory (default: current directory)")

    # List files command
    list_files_parser = subparsers.add_parser("list-files", help="List recent files in the channel")
    list_files_parser.add_argument("--limit", type=int, default=10, help="Number of files to list (default: 10)")

    args = parser.parse_args(args)

    if args.command == "upload":
        upload_image(args.image_path)
    elif args.command == "post":
        post_message(args.message)
    elif args.command == "history":
        messages = get_channel_messages(args.limit)
        if messages:
            for msg in messages:
                print(f"User: {msg.get('user')}, Message: {msg.get('text')}, Timestamp: {msg.get('ts')}")
        else:
            print("Failed to retrieve messages.")
    elif args.command == "get":
        get_file(args.file_id, args.output)
    elif args.command == "list-files":
        files = list_files(args.limit)
        if files:
            for file in files:
                print(f"ID: {file['id']}, Name: {file['name']}, Type: {file['filetype']}, Size: {file['size']} bytes, Created: {file['created']}")
        else:
            print("Failed to retrieve files.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()