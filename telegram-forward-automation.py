"""

Forwards files in batches(100 messages = 1 batch) without any cacheing from recent to older messages

"""


import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChat

# Retrieve API ID, API hash, and phone number from environment variables
api_id = int(os.getenv('appid'))
api_hash = os.getenv('hashid')
phone_number = os.getenv('number')

# Initialize the Telegram client
client = TelegramClient(phone_number, api_id, api_hash)

async def forward_files_in_batches(group_id, start_index=0, batch_size=100):
    await client.start()  # Connect to Telegram

    try:
        saved_messages = await client.get_entity('me')  # 'me' represents your saved messages
        target_group = await client.get_entity(PeerChat(group_id))

        while True:
            # Fetch the messages to be forwarded
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
                print("No more messages to forward.")
                break

            # Collect message IDs to forward (files and messages)
            message_ids = [message.id for message in messages]

            if not message_ids:
                print("No files to forward in this batch.")
                break

            # Forward messages to the specified group
            await client.forward_messages(
                entity=target_group,  # Target group entity
                from_peer=saved_messages,  # Source "Saved Messages"
                messages=message_ids  # List of message IDs to forward
            )
            print(f"Forwarded {len(message_ids)} messages to Group ID: {group_id}.")

            # Update the start index for the next batch
            start_index = messages[-1].id

            # Sleep to avoid hitting rate limits
            await asyncio.sleep(10)  # Sleep for 10 seconds

    except Exception as e:
        print(f"Failed to forward messages: {e}")

if __name__ == '__main__':
    # Define the target group ID
    group_id = groupid  # Replace with your actual group ID

    # Run the script to forward files in batches
    asyncio.run(forward_files_in_batches(group_id))