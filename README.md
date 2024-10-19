# Telegram Message Hub

Welcome to **Telegram Message Hub**! This project provides a robust solution for transferring Telegram messages from one source (like saved messages or a group) to a target group while maintaining the original message order and structure. It uses the [Telethon](https://docs.telethon.dev/) library for interacting with the Telegram API.

## Overview

The **Telegram Message Hub** project consists of three main components:
1. **Message Caching:** Collects and stores messages from a specified chat or saved messages, enabling access to older messages that are not directly accessible via the Telegram API.
2. **Message Forwarding (with caching):** Forwards cached messages to a target Telegram group while preserving the original order and structure.
3. **Direct Message Forwarding:** Forwards messages without caching, from recent to oldest dates.

## Why Caching is Necessary

Caching is crucial in this project for several reasons:
1. **Access to Older Messages:** Telegram API doesn't provide a straightforward way to access the oldest messages in a chat directly. Caching allows us to store these messages locally.
2. **Maintaining Hierarchical Structure:** To recreate the exact structure of messages in the target group, we need to forward them in the reverse order of how they were originally sent. Caching enables this by allowing us to process messages from oldest to newest.
3. **Efficient Processing:** Caching allows for batch processing and checkpointing, making the transfer process more reliable and resumable in case of interruptions.

>  [If you dont want to Cache, refer this](#direct-forwarding-without-caching)


## Features

- **Dynamic Caching:** Retrieve and cache messages from Telegram, enabling access to older messages.
- **Batch Processing:** Save messages in JSON files organized by batch for efficient handling.
- **Structure Preservation:** Forward messages from cached batches in reverse order to maintain the original message hierarchy in the target group.
- **Group Type Support:** Separate scripts for forwarding to normal groups and supergroups.
- **Direct Forwarding:** Option to forward messages without caching, from recent to oldest dates.
- **Robust Error Handling:** Includes retry mechanisms for API rate limits and errors.
- **Checkpoint System:** Resume processing from the last successful batch if interrupted.

## Prerequisites

To get started, you will need:
- Python 3.7 or higher
- [Telethon](https://docs.telethon.dev/) library
- Telegram API credentials (API ID and API Hash)
- A Telegram account for authentication

## Project Structure
```
.
├── cached_batches
│   └── batch_0.json
├── checkpoint.txt
├── telegram1.py
├── telegram2(normalgroup).py
├── telegram2(supergroup).py
└── telegram-forward-automation.py
```

## Setup

1. **Clone the Repository**

   Clone the repository and navigate to the project directory:
```
   git clone https://github.com/deekshith0509/TelegramMessageHub.git
   cd TelegramMessageHub
```
2. **Install Dependencies**

   Install the required Python packages:
```
   pip install -r requirements.txt
```
3. **Configure Environment Variables**

   Set up the environment variables for your Telegram API credentials:

   - `appid` - Your Telegram API ID
   - `hashid` - Your Telegram API Hash
   - `number` - Your phone number associated with Telegram

   You can set these variables in your terminal session or use a `.env` file with the python-dotenv package.
```
   export appid=your_api_id
   export hashid=your_api_hash
   export number=your_phone_number
````
## Usage

### Caching Messages

Run the following script to cache messages from your saved messages or a specific chat:
```
    python telegram1.py
```
This script connects to Telegram, retrieves messages (including older ones not directly accessible), and stores them in JSON files in the `cached_batches` directory.

### Forwarding Cached Messages

To forward cached messages to a target Telegram group, preserving the original structure:

For normal groups:
```
    python telegram2(normalgroup).py
```
For supergroups:
```
    python telegram2(supergroup).py
```
Note: Update the `group_id` variable in the respective script with the ID of the target group.

## Direct Forwarding (Without Caching)

For direct forwarding of messages from the most recent to the oldest, without utilizing caching, use the `telegram-forward-automation` script. This approach is notably faster compared to alternatives that rely on caching, as it performs message forwarding directly.

Telegram does not offer a direct method to access the oldest messages first. Instead, it provides access starting from the most recent messages. Therefore, for forwarding messages in reverse chronological order (from recent to oldest), follow these steps:

1. **Retrieve Recent Messages**: Start by fetching the latest messages from the source chat or channel. Telegram's API allows access to messages starting from the most recent and working backward.

2. **Forward Messages**: Use the `telegram-forward-automation` script to forward each retrieved message to the target chat or channel. The script will handle the forwarding process without the need for caching.

3. **Iterate Through Messages**: Continue fetching and forwarding messages until you have processed all the messages from the source, working from the most recent to the oldest.

### Benefits of Direct Forwarding Without Caching

- **Increased Speed**: Since caching is not used, the process is faster as it eliminates the overhead associated with storing and retrieving messages from a cache.
- **Simplicity**: The method is straightforward as it forwards messages directly, reducing complexity.
- **Real-Time Forwarding**: Messages are forwarded in real-time as they are retrieved, ensuring up-to-date processing.

By leveraging the `telegram-forward-automation` script, you can efficiently handle large volumes of messages, ensuring that the forwarding process is both effective and rapid.
strcuture

## Script Details

### telegram1.py

- **Purpose:** Retrieves and caches messages from Telegram, including older messages.
- **Features:**
  - Connects to Telegram and fetches messages in batches.
  - Saves messages as JSON files, maintaining their original order.
  - Handles rate limits and retries.
  - Uses checkpoints to resume from the last successful batch.

### telegram2(normalgroup).py and telegram2(supergroup).py

- **Purpose:** Forwards cached messages to a Telegram group (normal or super), preserving the original structure.
- **Features:**
  - Reads cached JSON files and forwards messages in reverse order to maintain hierarchy.
  - Implements retry logic for handling rate limits and errors.
  - Uses a checkpoint file to resume processing if interrupted.

## Error Handling

- **FloodWaitError:** Automatically handles rate limits by waiting and retrying.
- **JSONDecodeError:** Logs errors related to JSON parsing.

## Future Enhancements

- **User Interface:** Create a graphical or web-based interface for easier management.
- **Media Support:** Add functionality to handle various media types.
- **Scheduling:** Implement scheduling for automatic caching and forwarding.
- **Performance Optimization:** Enhance performance for handling larger datasets.


### **⚠️ Warning: API Limitations and Forwarding Constraints**
> 
> Please be aware that due to Telegram's API limitations, only approximately 1,800 messages can be forwarded per hour. If you attempt to forward more than 1,800 messages at a time, you may encounter issues due to these constraints.
> 
> **Important Points to Note:**
> - **Rate Limit**: The API restricts the number of messages that can be forwarded within an hour. This means that you will need to wait until the hour limit resets to continue forwarding additional messages.
> - **Checkpoints**: The `telegram2` scripts are designed to handle API limits efficiently by using checkpoints. This ensures that if the API limit is exceeded, the script will maintain progress and resume forwarding messages from where it left off.

> By understanding these limitations and using the provided scripts, you can effectively manage the forwarding process while adhering to API restrictions. If the API limit is exceeded, simply rerun the `telegram2($grouptype)` script after an hour. The script dynamically updates `checkpoint.txt` at runtime, ensuring that it continues from where it left off. This provides an automated, seamless workflow without the need for redundant processes or manual intervention.



## Contributing

Contributions are welcome! If you have ideas for improvements or find any issues, please open an issue or submit a pull request.
## Acknowledgments

- Telethon for providing the Telegram API library.
- Python's asyncio for asynchronous programming.

Feel free to reach out with any questions or feedback!

