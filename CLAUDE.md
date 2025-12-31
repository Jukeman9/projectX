# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A command-line chat application using OpenAI's API. This is a beginner's first Python project - prioritize learning and understanding over quick fixes.

## Teaching Guidelines

When helping with this codebase:

- **Explain concepts in simple terms** - avoid jargon, define new terms when introduced
- **Break down problems into smaller steps** - don't jump to complex solutions
- **Explain the "why"** - not just what code does, but why it's written that way
- **Use comments in code** - help document what's happening for learning purposes
- **Guide toward solutions** - help discover answers rather than always providing them directly
- **Encourage good practices** - explain why they matter (e.g., why use functions, why handle errors)
- **Be patient with mistakes** - explain what went wrong and how to fix it

## Commands

```bash
# Run the application
python main.py

# Install dependencies (uses uv, based on pyproject.toml)
uv sync
```

## Architecture

Single-file application (`main.py`) with the following flow:

1. **Menu loop** - Main entry point offering: open chat, print history, or quit
2. **Chat loop** (`chat_open()`) - Interactive conversation with OpenAI API
3. **Response parsing** (`parse_ai_response()`) - Extracts text from API responses
4. **Persistence** - Chat history saved to `chat_history.json` after each turn

### Key Data Structures

- `chat_history`: List of message dicts with role, content, turn_id, timestamp, type
- User messages use hardcoded `"type": "text"`
- AI messages use dynamic `message.type` from OpenAI API

### Dependencies

- `openai` - API client
- `python-dotenv` - Loads `.env` file for API key (`OPENAI_API_KEY`)

## Environment Setup

Requires `.env` file with:
```
OPENAI_API_KEY=your_key_here
```

## Known Technical Debt

Documented in README.md:
1. **Multimodal response handling** - Currently assumes text-only responses
2. **Type inconsistency** - User vs AI message type field handling differs

## Python Concepts in This Project

Key concepts to understand and reinforce:

- **Functions** - `parse_ai_response()`, `save_chat()`, `load_chat()`, `chat_open()`
- **Global variables** - `chat_history`, `turn_id`, `app_open` (discuss when globals are okay vs alternatives)
- **Lists and dictionaries** - chat_history is a list of dicts
- **File I/O** - reading/writing JSON with `open()` and context managers (`with`)
- **While loops** - both the menu loop and chat loop
- **API calls** - using the OpenAI client library
- **Environment variables** - keeping secrets out of code with `.env`

## Good Learning Opportunities

When making changes, consider discussing:

- Error handling with try/except (currently minimal)
- Breaking into multiple files as the project grows
- Type hints for better code clarity
- Input validation
