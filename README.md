# Chat Application

A simple command-line chat application using OpenAI's API.

## Current Status

This is a learning project demonstrating basic OpenAI API integration.

## Known Issues & Future Improvements

### 1. Multimodal Response Handling
**Location**: `main.py:parse_ai_response()` and response processing logic
**Issue**: Currently assumes all AI responses are text-only
**Impact**: Cannot handle images, videos, or mixed content from OpenAI responses
**Priority**: High (breaks functionality with non-text responses)
**Status**: Deferred - documented for future implementation

**Technical Details**:
- User inputs stored with hardcoded `"type": "text"`
- AI responses use dynamic `message.type` from OpenAI API
- Parsing logic assumes `message.content[0].text` structure
- Need to implement content type detection and appropriate handlers

**Related Code**:
- Lines 53-56: Response parsing logic
- Lines 58-73: AI output object creation

### 2. Chat History Type Inconsistency
**Location**: `main.py:chat_history` data structure
**Issue**: Inconsistent type field usage between user and AI messages
**Impact**: Makes data processing and serialization inconsistent
**Priority**: Medium
**Status**: Identified - needs standardization

## Architecture

### Data Flow
1. User input → stored as text message in chat_history
2. OpenAI API call → response received
3. Response parsing → assumes text content only
4. AI output → stored in chat_history with mixed type system

### Current Limitations
- Single-modal responses only
- Hardcoded type assumptions
- No error handling for unsupported content types
