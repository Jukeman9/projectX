"""
Chat Application with OpenAI Integration

A simple command-line chat application demonstrating OpenAI API usage.

KNOWN ISSUES & TECHNICAL DEBT:
=============================

See README.md for detailed issue tracking and future improvements.

1. MULTIMODAL RESPONSE HANDLING (HIGH PRIORITY)
   - Location: parse_ai_response() function and response processing
   - Issue: Assumes all AI responses are text-only content
   - Current: Hard-coded text extraction from message.content[0].text
   - Future: Need to handle images, videos, mixed content based on message.type

2. CHAT HISTORY TYPE INCONSISTENCY (MEDIUM PRIORITY)
   - Location: chat_history data structure throughout file
   - Issue: User messages use "type": "text", AI messages use message.type
   - Impact: Inconsistent data structure for serialization/storage

For detailed technical specifications, see README.md
"""

from datetime import datetime
from re import ASCII
import time
import json
import random
import string
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(base_url="http://localhost:11434/v1")

chat_content = []
chat_history = []
chat_index = []
chat_id = None
turn_id = 0
app_open = True
OLLAMA_MODEL = "gemma3:4b"
OPENAI_MODEL = "gpt-5-nano"
CHAT_MODEL = OLLAMA_MODEL
MAX_CONTEXT_TOKENS = 200000


# Create the chats directory if it doesn't exist
os.makedirs("chats", exist_ok=True)


# That loads chat history - we need to pass it when loading chat from the menu
def load_chat(chat_id):
    global chat_history
    try:
        with open(f"chats/{chat_id}.json", mode="r", encoding="UTF-8") as f:
            chat_history = json.load(f)
    except FileNotFoundError:
        chat_history = []


def show_chat_history():
    print("\n")
    if chat_history:
        for message in chat_history:
            if message["role"] == "user":
                print(f"User:{message['content']['text']}")
            elif message["role"] == "assistant":
                print(f"AI:{message['content']['text']}")


# We should get turn ids when loading the chat from the menu as well.
def get_turn_id():
    return chat_history[-1]["turn_id"] if chat_history else 0


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
        "text": response_message.content[0].text
    }


def unix_time_to_readable(unix_timestamp):
    """Convert unix timestamp to a human redable date format

    Args:
        unix_timestamp (_type_): _description_
    """
    return datetime.fromtimestamp(unix_timestamp).strftime("%Y-%m-%d %H:%M:%S")


def generate_string(length):
    """Generatea a random string of specified length"""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def generate_chat_id(num_words, word_length):
    """
    Generate a chat ID with multiple random words joined by dashes.

    Args:
        num_words: How many words to generate (e.g., 3)
        word_length: How long each word should be (e.g., 6)

    Returns:
        A string like 'abcdef-xyzabc-mnopqr'
    """
    words = [generate_string(word_length) for i in range(num_words)]
    return "-".join(words)


def index_chat():
    global chat_id
    chat_index = {
        "id": generate_chat_id(num_words=3, word_length=4),
        "title": chat_history[0]["content"]["text"][:30],
        "time_created": chat_history[0]["timestamp"],
    }
    chat_id = chat_index["id"]
    return chat_index


def save_index():
    with open("chats/chat_index.json", mode="w", encoding="UTF-8") as f:
        json.dump(chat_index, f, indent=2, ensure_ascii=False)


def load_index():
    global chat_id, chat_index
    """Loads the chats from chat_index.json into a nicely formatted table."""

    with open("chats/chat_index.json", mode="r", encoding="UTF-8") as f:
        chat_index = json.load(f)

        # Header
        print("\n" + "=" * 60)
        print(f"{'#':<4} {'Chat title':<35} {'Created at':<20}")
        print("=" * 60)

        # Chat list
        for i, chat in enumerate(chat_index, start=1):
            title = (
                chat["title"][:32] + "..." if len(chat["title"]) > 35 else chat["title"]
            )
            timestamp = unix_time_to_readable(chat["time_created"])
            num = f"{i}."
            print(f"{num:<4} {title:<35} {timestamp:<20}")
        print("=" * 60 + "\n")

        print("\nResume previous chat or create new\n")
        app_input = input(
            "Enter chat number or type '/new' or '/n' to start a new one ('/q' or '/quit' to quit): "
        )
        if app_input.isdigit() and 1 <= int(app_input) <= len(chat_index):
            chat_num = chat_index[int(app_input) - 1]
            chat_id = chat_num["id"]
        elif app_input.lower() in ["/new", "/n"]:
            chat_id = None
            print("\n" + "=" * 60 + "\n\nNew chat")
        elif app_input.lower() in ["/quit", "/q"]:
            return False  # Exit the main loop
        else:
            print("Invalid choice, try again")
        return True


def save_chat():
    global chat_id
    with open(f"chats/{chat_id}.json", mode="w") as f:
        json.dump(chat_history, f, indent=2, ensure_ascii=False)


# def load_chat():
#     global chat_id
#     with open(f"chats/{chat_id}.json", mode="r") as f:
#         chat = json.load(f)
#         print(chat)


def chat_open():
    global turn_id, chat_history, chat_content

    # Begin the chat with the last turn
    turn_id = get_turn_id()

    while True:
        turn_id += 1

        new_input = input("\nUser (or '/q' or /quit' to quit): ")

        if new_input.lower() in ["/q", "/quit"]:
            print("Returning to menu")
            break

        print("-" * 10)

        if chat_history and "usage" in chat_history[-1]:  # Count tokens
            last_token_count = chat_history[-1]["usage"]["total tokens"]
            token_sum = last_token_count + (len(new_input) / 4)
        else:
            token_sum = len(new_input)

        # Add user input to chat history
        chat_history.append(
            {
                "content": {"text": new_input},
                "role": "user",
                "turn_id": turn_id,
                "status": "completed",
                "timestamp": float(int(time.time())),
                "type": "text",
            }
        )
        # Index chat if chat_history is empty
        if len(chat_history) <= 1:
            chat_index.append(index_chat())
            save_index()

        # Save chat after user sends input
        save_chat()

        chat_content = [
            {"role": message["role"], "content": message["content"]["text"]}
            for message in chat_history
        ]

        # Creating an AI reply from user input if token count not exceeded
        if token_sum < MAX_CONTEXT_TOKENS:
            response = client.responses.create(
                model=CHAT_MODEL,
                input=chat_content,
            )
        else:
            print("Number of tokens exceeded, start a new chat")
            continue

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
        print(f"AI: {response_data['text']}")
        print("-" * 10)
        # print("Response:\n")
        # print(response)
        # print("-" * 10)
        # print("Chat history:\n")
        # print(chat_history)
        print("-" * 10)
        print("Chat content:\n")
        print(chat_content)
        # print("-" * 10)
        print("Chat token count:\n")
        print(token_sum)


# def index_open():


while app_open:
    should_continue = load_index()
    if not should_continue:
        break  # Exit the app

    load_chat(chat_id)
    show_chat_history()
    chat_open()
    # print("What do you want to do?")
    # print("1. Chat")
    # print("2. Start a new chat")
    # # print("2. Print the chat history")
    # print("o. switch to OpenAI API")
    # print("q. Quit the app")
    # app_input = input("Your choice: ")
    # if app_input == "1":
    #     chat_open()  # that opened the chat_history
    # # here we need to load the list of chats and display to the user.
    # # or even better would be to have another loop that comes in here that does the job
    # #
    # # elif app_input == "2":
    # #     load_chat()
    # elif app_input == "o":
    #     client = OpenAI()
    #     CHAT_MODEL = OPENAI_MODEL
    # elif app_input == "q":
    #     print("Quitting...")
    #     break
