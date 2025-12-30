"""
Chat Application with OpenAI Integration

A simple command-line chat application demonstrating OpenAI API usage.

KNOWN ISSUES & TECHNICAL DEBT:
=============================

See README.md for detailed issue tracking and future improvements.

1. MULTIMODAL RESPONSE HANDLING (HIGH PRIORITY)
   - Location: parse_ai_response() function and response processing (lines ~53-73)
   - Issue: Assumes all AI responses are text-only content
   - Current: Hard-coded text extraction from message.content[0].text
   - Future: Need to handle images, videos, mixed content based on message.type

2. CHAT HISTORY TYPE INCONSISTENCY (MEDIUM PRIORITY)
   - Location: chat_history data structure throughout file
   - Issue: User messages use "type": "text", AI messages use message.type
   - Impact: Inconsistent data structure for serialization/storage

For detailed technical specifications, see README.md
"""

# import datetime
import time
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def parse_ai_response(response_message):
    """
    Parse AI response content from OpenAI API response.

    TECHNICAL DEBT: MULTIMODAL RESPONSE HANDLING
    ============================================
    **Issue ID**: MULTIMODAL_RESPONSE_HANDLING (See README.md)
    **Priority**: HIGH
    **Status**: DEFERRED - Current implementation assumes text-only responses

    CURRENT LIMITATIONS:
    -------------------
    - Assumes response_message.content[0] exists and is text type
    - No handling for image_file, video_file, or other content types
    - No validation of response_message.type before accessing content
    - Will fail if OpenAI returns non-text content

    FUTURE IMPLEMENTATION NEEDED:
    ----------------------------
    - Check response_message.type to determine content type
    - Handle 'text' content: response_message.content[0].text
    - Handle 'image_file' content: response_message.content[0].image_file
    - Handle mixed content arrays
    - Return appropriate data structure for each type

    Args:
        response_message: OpenAI response message object with content array

    Returns:
        dict: Parsed response data with 'response_text' key (for now)

    Raises:
        IndexError: If response_message.content is empty
        AttributeError: If content doesn't have expected text attribute
    """
    # FIXME: This implementation has known limitations documented above
    # TODO: Implement proper content type detection and parsing
    return {
        # WARNING: Assumes text-only content - will break with images/videos
        "response_text": response_message.content[0].text
    }


# def unix_time_to_readable(unix_timestamp):
#     """Convert unix timestamp to a human redable date format

#     Args:
#         unix_timestamp (_type_): _description_
#     """
#     return datetime.fromtimestamp(unix_timestmap).strftime("%Y-%m-%d %H:%M:%S")

chat_history = []
turn_id = 0
app_open = True


def save_chat():
    with open("chat_history.json", mode="w") as f:
        json.dump(chat_history, f, indent=2, ensure_ascii=False)


def load_chat():
    with open("chat_history.json", mode="r") as f:
        chat = json.load(f)
        print(chat)


def chat_open():
    global turn_id, chat_history
    while True:
        # Begin the chat with turn 1
        turn_id += 1

        chat_input = input("\nUser (or '/q' or /quit' to quit): ")

        if chat_input.lower() in ["/q", "/quit"]:
            print("Returning to menu")
            break

        print("-" * 10)

        # Add user input to chat history
        chat_history.append(
            {
                "content": chat_input,
                "role": "user",
                "turn_id": turn_id,
                "status": "completed",
                "timestamp": float(int(time.time())),
                "type": "text",
            }
        )

        # Creating an AI reply from user input
        response = client.responses.create(
            model="gpt-4.1-nano",
            input=chat_input,
        )

        # Save the response message to variable
        message = response.output[0]

        # Extract the AI reply
        response_data = parse_ai_response(message)

        # Create an AI output object to save to history
        # NOTE: Type inconsistency - see CHAT_HISTORY_TYPE_INCONSISTENCY in README.md
        ai_output = {
            "role": message.role,
            "content": response_data,  # May be incomplete due to multimodal limitations
            "status": message.status,
            "type": message.type,  # Dynamic type vs user's hardcoded "text"
            "timestamp": response.created_at,
            "response_id": response.id,
            "model": response.model,
            "usage": {
                "input tokens": response.usage.input_tokens,
                "output tokens": response.usage.output_tokens,
                "total tokens": response.usage.total_tokens,
            },
            "turn_id": turn_id,
        }

        # Add ai output to chat history
        chat_history.append(ai_output)
        save_chat()

        # Display the response text
        print(f"AI: {response_data['response_text']}")
        print("-" * 10)
        print("Response:\n")
        print(response)
        print("-" * 10)
        print("Chat history:\n")
        print(chat_history)


while app_open:
    print("What do you want to do?")
    print("1. Open chat")
    print("2. Print the chat history")
    print("q. Quit the app")
    app_input = input("Your choice: ")
    if app_input == "1":
        chat_open()
    elif app_input == "2":
        load_chat()
    elif app_input == "q":
        print("Quitting...")
        break
