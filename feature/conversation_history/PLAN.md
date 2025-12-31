# Plan: Add Conversation History to Chat

## Goal
Enable the AI to remember previous messages in the conversation by passing chat history to the API.

## Key Decisions Made
- Keep using Responses API (already working, can swap later for Ollama etc.)
- Two "views" of data: full `chat_history` for storage, stripped `messages` array for API
- Token limit: `MAX_CONTEXT_TOKENS = 200000` with error when exceeded
- Caching: Automatic by OpenAI (activates at 1024+ tokens), just display `cached_tokens` in output

## Files to Modify
- `main.py` - all changes in this single file

---

## Implementation Steps

### Step 1: Add Configuration Variable
Add `MAX_CONTEXT_TOKENS = 200000` near the top of the file with other globals.

**Difficulty: Easy**

---

### Step 2: Create `build_messages_for_api()` Function
A new function that:
- Takes `chat_history` as input
- Loops through and extracts only `role` and `content` for each message
- Returns a list of simple `{"role": "...", "content": "..."}` dicts
- Handles the difference between user messages (content is string) and AI messages (content is dict with response_text)

**Difficulty: Medium** - The tricky part is handling the different content formats

**Concepts to practice:**
- Writing functions with parameters
- Looping through lists
- Checking data types with `isinstance()`
- Building new lists from existing data

---

### Step 3: Create `count_tokens_estimate()` Function
A rough estimate function:
- Simple approach: count characters and divide by 4 (rough token estimate)
- This is good enough for now - can improve later with tiktoken library

**Difficulty: Easy**

**Concepts to practice:**
- `len()` function
- Integer division `//`

---

### Step 4: Modify `chat_open()` Function
Before the API call:
1. Build the messages array using `build_messages_for_api()`
2. Add the current user input to the messages array
3. Check if estimated tokens exceed `MAX_CONTEXT_TOKENS` - if yes, print error and skip API call
4. Pass the full messages array to `client.responses.create(input=messages)`

**Difficulty: Medium** - You need to find the right place in the existing code

**Key change:**
```python
# OLD
input=chat_input

# NEW
input=messages
```

---

### Step 5: Update Debug Output
After the API call, print `cached_tokens` from the response usage to see caching in action.

**Difficulty: Easy** - Just add a print statement

---

## Testing Your Implementation

1. **Basic test:** Start a chat, send "Hello my name is [your name]"
2. **Memory test:** Send "What is my name?" - AI should remember!
3. **Multi-turn test:** Have a 3-4 message conversation about a topic, then ask "What have we been talking about?"

## If You Get Stuck

1. First, add print statements to debug (see code_examples.py)
2. Check the "Common Mistakes" section in code_examples.py
3. Then look at the specific code example for that step
4. If still stuck, ask for help - that's what I'm here for!

## What You'll Learn

- **Functions:** Creating reusable code blocks
- **Data transformation:** Converting one data structure to another
- **Conditional logic:** Checking types and values
- **API integration:** How APIs expect data formatted
- **Debugging:** Using print statements to understand data flow
