# import datetime
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


# def unix_time_to_readable(unix_timestamp):
#     """Convert unix timestamp to a human redable date format

#     Args:
#         unix_timestamp (_type_): _description_
#     """
#     return datetime.fromtimestamp(unix_timestmap).strftime("%Y-%m-%d %H:%M:%S")


chat_open = True
chat_history = []
turn_id = 0

while chat_open:
    # Begin the chat with turn 1
    turn_id += 1

    user_input = input("User: ")

    # Add user input to chat history
    chat_history.append(
        {
            "content": user_input,
            "role": "user",
            "turn_id": turn_id,
            "status": "completed",
            "timestamp": float(int(time.time())),
            "type": "text",
        }
    )
    print("\n")

    # Creating an AI reply from user input
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=user_input,
    )

    # Save the response messag to variable
    message = response.output[0]

    # Extract the AI reply
    response_data = {
        # Extract the AI text reply , can be extended for other response data
        "response_text": message.content[0].text
    }

    # Create an AI output object to save to history
    ai_output = {
        "role": message.role,
        "content": response_data,
        "status": message.status,
        "type": message.type,
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

    # Display the response text
    print(response_data["response_text"])
    print("-" * 10)
    print(response)
    print(chat_history)
