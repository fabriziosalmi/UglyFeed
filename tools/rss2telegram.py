import argparse
import feedparser
import requests
import time
import os

# Constants
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'
LATEST_ENTRY_ID_FILE = 'latest_entry_id.txt'
SLEEP_INTERVAL = 600  # 10 minutes


def send_telegram_message(bot_token, chat_id, message):
    """Send a message to the specified Telegram chat."""
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    return response.json()


def get_latest_entry_id(file_path):
    """Retrieve the latest entry ID from the specified file."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    return None


def save_latest_entry_id(file_path, entry_id):
    """Save the latest entry ID to the specified file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(entry_id)


def process_feed(rss_feed_url, bot_token, chat_id, latest_entry_id_file):
    """Parse the RSS feed and send new entries to Telegram."""
    feed = feedparser.parse(rss_feed_url)
    latest_entry_id = get_latest_entry_id(latest_entry_id_file)

    for entry in reversed(feed.entries):
        if entry.id != latest_entry_id:
            message = f'<b>{entry.title}</b>\n{entry.link}'
            send_telegram_message(bot_token, chat_id, message)
            save_latest_entry_id(latest_entry_id_file, entry.id)
        else:
            break


def main():
    """Main function to parse arguments and start the feed processing loop."""
    parser = argparse.ArgumentParser(description='RSS to Telegram Bot')
    parser.add_argument('rss_feed_url', help='The URL of the RSS feed')
    args = parser.parse_args()

    while True:
        process_feed(args.rss_feed_url, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, LATEST_ENTRY_ID_FILE)
        time.sleep(SLEEP_INTERVAL)


if __name__ == '__main__':
    main()