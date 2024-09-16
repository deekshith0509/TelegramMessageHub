"""
Used to cache the messages into proper formatted objects for forwarding in the batchwise.

"""

import os
import asyncio
import json
import re
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChat

# Retrieve API ID, API hash, and phone number from environment variables
api_id = int(os.getenv('appid'))
api_hash = os.getenv('hashid')
phone_number = os.getenv('number')

# Initialize the Telegram client
client = TelegramClient(phone_number, api_id, api_hash)

# Directories for caching and forwarding
CACHE_DIR = 'cached_batches'
os.makedirs(CACHE_DIR, exist_ok=True)

def extract_batch_number(filename):
    match = re.search(r'batch_(\d+)\.json', filename)
    if match:
        return int(match.group(1))
    return -1

async def cache_messages():
    await client.start()  # Connect to Telegram
    print("Started caching messages...")

    try:
        saved_messages = await client.get_entity('me')  # 'me' represents your saved messages
        start_index = 0
        batch_size = 100
        batch_number = 0

        while True:
            history = await client(GetHistoryRequest(
                peer=saved_messages,
                limit=batch_size,
                offset_id=start_index,
                offset_date=None,
                add_offset=0,
                max_id=0,
                min_id=0,
                hash=0
            ))

            messages = history.messages
            if not messages:
                print("No more messages to cache.")
                break

            # Sort messages in reverse order by their ID
            messages.sort(key=lambda msg: msg.id, reverse=True)

            batch_data = [{
                "id": msg.id,
                "date": msg.date.isoformat(),
                "message": msg.message,
                "media": {
                    "type": msg.media.__class__.__name__,
                    "data": None  # You can add handling for media if required
                }
            } for msg in messages]

            batch_path = os.path.join(CACHE_DIR, f'batch_{batch_number}.json')
            with open(batch_path, 'w') as f:
                json.dump(batch_data, f, indent=4)

            print(f"Cached {len(messages)} messages in {batch_path}.")
            start_index = messages[-1].id
            batch_number += 1
            await asyncio.sleep(10)  # Sleep to avoid hitting rate limits

        print("Finished caching messages.")

    finally:
        await client.disconnect()

if __name__ == '__main__':
    # Define the target group ID
    group_id = groupid # Replace with your actual group ID

    # Run the caching and forwarding process
    asyncio.run(cache_messages())
