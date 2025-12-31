"""
CODE EXAMPLES: Conversation History Feature
============================================

These are reference examples to help you implement the feature.
TRY TO CODE IT YOURSELF FIRST! Only look here when stuck.

The examples are organized by step - scroll down as needed.
"""

# =============================================================================
# STEP 1: Configuration Variable
# =============================================================================
# This is simple - just add this near your other global variables

MAX_CONTEXT_TOKENS = 200000  # Maximum tokens before showing an error


# =============================================================================
# STEP 2: build_messages_for_api() Function
# =============================================================================
# This function transforms your rich chat_history into simple messages for the API
#
# YOUR CHALLENGE:
# - Loop through chat_history
# - For each message, extract just "role" and "content"
# - Handle the fact that user content is a string, but AI content is a dict
#
# HINT: Look at your current chat_history structure:
#   User message: {"role": "user", "content": "hello", ...other stuff...}
#   AI message:   {"role": "assistant", "content": {"response_text": "hi"}, ...}

def build_messages_for_api(chat_history):
    """
    Convert chat_history to the simple format the API expects.

    Args:
        chat_history: List of message dicts with full metadata

    Returns:
        List of simple {"role": "...", "content": "..."} dicts
    """
    messages = []  # Start with empty list

    for message in chat_history:
        # Get the role (same for both user and AI)
        role = message["role"]

        # Get the content - this is different for user vs AI messages!
        # User messages: content is a string like "hello"
        # AI messages: content is a dict like {"response_text": "hi there"}

        raw_content = message["content"]

        # Check if content is a dictionary (AI message) or string (user message)
        if isinstance(raw_content, dict):
            # It's an AI message - extract the actual text
            content = raw_content["response_text"]
        else:
            # It's a user message - content is already a string
            content = raw_content

        # Add the simplified message to our list
        messages.append({
            "role": role,
            "content": content
        })

    return messages


# =============================================================================
# ALTERNATIVE: Using a list comprehension (more advanced, same result)
# =============================================================================
# This does the same thing in fewer lines - learn this pattern later!

def build_messages_for_api_compact(chat_history):
    """Same function but using list comprehension."""
    return [
        {
            "role": msg["role"],
            "content": msg["content"]["response_text"] if isinstance(msg["content"], dict) else msg["content"]
        }
        for msg in chat_history
    ]


# =============================================================================
# STEP 3: count_tokens_estimate() Function
# =============================================================================
# A rough way to estimate tokens without external libraries
#
# RULE OF THUMB: 1 token ≈ 4 characters in English
# This is not exact, but good enough for a safety check

def count_tokens_estimate(messages):
    """
    Estimate the number of tokens in a messages list.

    Args:
        messages: List of {"role": "...", "content": "..."} dicts

    Returns:
        Estimated token count (integer)
    """
    total_characters = 0

    for message in messages:
        # Count characters in the content
        total_characters += len(message["content"])
        # Also count the role (small but adds up)
        total_characters += len(message["role"])

    # Divide by 4 to estimate tokens
    estimated_tokens = total_characters // 4  # // is integer division

    return estimated_tokens


# =============================================================================
# STEP 4: Modified chat_open() - The Key Changes
# =============================================================================
# You don't need to rewrite the whole function!
# Just add these pieces in the right places.

# BEFORE the API call (after getting user input, before client.responses.create):

"""
# Build the messages array from chat history
messages = build_messages_for_api(chat_history)

# Add the current user input to the messages
messages.append({
    "role": "user",
    "content": chat_input
})

# Check if we're over the token limit
estimated_tokens = count_tokens_estimate(messages)
if estimated_tokens > MAX_CONTEXT_TOKENS:
    print(f"Error: Context window full! ({estimated_tokens} estimated tokens)")
    print(f"Maximum allowed: {MAX_CONTEXT_TOKENS} tokens")
    print("Start a new chat or implement conversation summarization.")
    continue  # Skip this turn and ask for new input
"""

# THE API CALL - change input from string to messages list:

"""
# OLD (current code):
response = client.responses.create(
    model="gpt-4.1-nano",
    input=chat_input,  # <-- just the current message
)

# NEW (with history):
response = client.responses.create(
    model="gpt-4.1-nano",
    input=messages,  # <-- full conversation history + current message
)
"""


# =============================================================================
# STEP 5: Display Cached Tokens (Debug Output)
# =============================================================================
# Add this after printing usage info to see caching in action

"""
# Check if cached_tokens info is available and print it
if hasattr(response.usage, 'prompt_tokens_details'):
    cached = response.usage.prompt_tokens_details.cached_tokens
    print(f"Cached tokens: {cached}")
    if cached > 0:
        print("Cache hit! You're saving money on these tokens.")
"""


# =============================================================================
# FULL EXAMPLE: What the messages array looks like
# =============================================================================
# This is what you're building and sending to the API:

example_messages = [
    {"role": "user", "content": "Hello, who are you?"},
    {"role": "assistant", "content": "I'm an AI assistant. How can I help you today?"},
    {"role": "user", "content": "What did I just ask you?"},
    # The AI will now see the full conversation and can answer correctly!
]


# =============================================================================
# DEBUGGING TIP
# =============================================================================
# If something isn't working, add print statements to see what's happening:

"""
print("=== DEBUG ===")
print(f"Number of messages in history: {len(chat_history)}")
print(f"Messages being sent to API: {messages}")
print(f"Estimated tokens: {estimated_tokens}")
print("=============")
"""


# =============================================================================
# COMMON MISTAKES TO AVOID
# =============================================================================
"""
1. Forgetting that AI content is nested: msg["content"]["response_text"]
   - User content is just: msg["content"]

2. Modifying chat_history directly when building messages
   - Always create a NEW list, don't modify the original

3. Not adding the current user input to messages before the API call
   - messages = build_messages_for_api(chat_history)  # history only
   - messages.append({"role": "user", "content": chat_input})  # + current!

4. Forgetting 'continue' after the token limit error
   - Without it, the code will try to call the API anyway
"""
