import os
import json
import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError
import re

# Retrieve API ID, API hash, and phone number from environment variables
api_id = int(os.getenv('appid'))
api_hash = os.getenv('hashid')
phone_number = os.getenv('number')

# Initialize the Telegram client
client = TelegramClient(phone_number, api_id, api_hash)

# Directory where cached messages are stored
CACHE_DIR = 'cached_batches'
CHECKPOINT_FILE = 'checkpoint.txt'

def extract_batch_number(filename):
    """ Extract batch number from filename. """
    match = re.search(r'batch_(\d+)\.json', filename)
    if match:
        return int(match.group(1))
    return -1

def read_checkpoint():
    """ Read the last processed batch file from the checkpoint file. """
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            return f.read().strip()
    return None

def write_checkpoint(batch_file):
    """ Write the last processed batch file to the checkpoint file. """
    with open(CHECKPOINT_FILE, 'w') as f:
        f.write(batch_file)

async def forward_cached_messages(group_id):
    await client.start()  # Connect to Telegram
    print("Started forwarding messages...")

    try:
        # Resolve the target group entity, which could be a channel (supergroup) or chat
        target_group = await client.get_entity(group_id)
        print(f"Resolved target group: {target_group}")

        # Get a sorted list of batch files based on their numerical suffixes in descending order
        batch_files = sorted(os.listdir(CACHE_DIR), key=extract_batch_number, reverse=True)

        # Read the checkpoint to find the last processed batch file
        last_processed_file = read_checkpoint()

        # If a checkpoint exists, resume from that file
        if last_processed_file:
            try:
                start_index = batch_files.index(last_processed_file)
                batch_files = batch_files[start_index:]  # Resume from the checkpoint
            except ValueError:
                print(f"Checkpoint file {last_processed_file} not found in directory.")
                # If checkpoint file is not found, proceed from the first file in sorted order

        # Process files in reverse order
        for batch_file in batch_files:
            batch_path = os.path.join(CACHE_DIR, batch_file)
            try:
                with open(batch_path, 'r') as f:
                    messages = json.load(f)

                # Sort messages in reverse order by their ID for this batch
                messages.sort(key=lambda msg: msg['id'], reverse=True)

                # Collect message IDs to forward
                message_ids = [msg['id'] for msg in messages]
                if not message_ids:
                    continue

                retry_attempts = 3
                while retry_attempts > 0:
                    try:
                        # Forward messages
                        await client.forward_messages(
                            entity=target_group,
                            from_peer='me',
                            messages=message_ids
                        )
                        print(f"Forwarded messages from {batch_file} to Group ID: {group_id}.")
                        
                        # Write to checkpoint after successful processing
                        write_checkpoint(batch_file)
                        break  # Break out of retry loop if successful

                    except FloodWaitError as e:
                        print(f"FloodWaitError occurred: {e}.")
                        
                        # Suggest the user try again after the wait period
                        wait_time = max(e.seconds, 3600)  # Ensure the wait time is at least 1 hour
                        print(f"Terminating process. Please try again after {wait_time // 3600} hour(s).")
                        
                        # Write the current checkpoint before terminating
                        write_checkpoint(batch_file)
                        return  # Gracefully terminate the process

                    except Exception as e:
                        print(f"Failed to forward messages from {batch_file}: {e}.")
                        break  # Break out of retry loop if a non-recoverable error occurs

                if retry_attempts == 0:
                    print(f"Failed to forward messages from {batch_file} after several attempts.")
                    break  # Stop processing further if retries exhausted

            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON from {batch_file}: {e}")
            except Exception as e:
                print(f"Error processing {batch_file}: {e}")
            
            # Sleep for 10 seconds between batches
            await asyncio.sleep(10)

        print("Finished forwarding messages.")

    except asyncio.CancelledError:
        print("Process was cancelled.")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    # Define the target group ID
    group_id = supergroupid  # Use the correct supergroup ID

    try:
        # Run the script to forward cached messages
        asyncio.run(forward_cached_messages(group_id))
    except KeyboardInterrupt:
        print("Process interrupted by user.")
