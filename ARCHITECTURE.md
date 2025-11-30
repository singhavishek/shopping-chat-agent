# Architecture & Implementation Guide

## Overview
The **Mobile Shopping Chat Agent** is a conversational AI application designed to assist users in discovering and comparing mobile phones. It leverages a Large Language Model (LLM) via the **Groq API** to understand natural language queries and dynamically interact with a structured product database.

## System Architecture

The application follows a modular architecture separating the UI, Agent Logic, and Data Layer.

```mermaid
graph TD
    User[User] <--> UI[Streamlit UI (app.py)]
    UI <--> Agent[ShoppingAgent (src/chatbot.py)]
    Agent <--> Groq[Groq API (LLM)]
    Agent <--> DB[PhoneDB (src/phone_db.py)]
    DB <--> JSON[(data/phones.json)]
```

## Components

### 1. Frontend Layer (`app.py`)
Built with **Streamlit**, this layer handles user interaction and state management.
- **Chat Interface**: Uses `st.chat_message` and `st.chat_input` for a modern conversational UI.
- **Session State**: Maintains conversation history (`st.session_state.messages`) across re-runs.
- **Streaming**: Simulates a typing effect for better user experience.
- **Error Handling**: Catches configuration errors (e.g., missing API keys) and displays user-friendly alerts.

### 2. Agent Layer (`src/chatbot.py`)
This is the core logic engine, implemented in the `ShoppingAgent` class.
- **LLM Integration**: Connects to the **Groq API** using the `openai/gpt-oss-20b` model.
- **Tool Definitions**: Defines function schemas (JSON) for `search_phones`, `get_phone_details`, and `compare_phones` that the LLM can invoke.
- **Multi-Turn Reasoning**: Implements a loop in `send_message` to handle complex queries requiring multiple steps (e.g., Search -> Get Details -> Answer).
- **System Prompt**: Enforces the persona, safety rules, and formatting guidelines (Markdown tables, currency, etc.).

### 3. Data Layer (`src/phone_db.py`)
Abstractions for data access.
- **PhoneDB Class**: Loads data from `data/phones.json` upon initialization.
- **Search Logic**: Implements keyword matching and filtering (price, brand) in Python.
- **Retrieval**: Provides methods to fetch specific phones by ID or batch IDs for comparison.

### 4. Data Source (`data/phones.json`)
A JSON file acting as a mock database.
- Contains 50+ records of popular mobile phones.
- Schema includes: `id`, `name`, `brand`, `price`, `specs` (camera, battery, display, processor, storage), and `description`.

## Key Workflows

### Search Workflow
1. **User Query**: "Best camera phone under 30k"
2. **LLM Analysis**: The model analyzes the intent and decides to call `search_phones(query='camera', max_price=30000)`.
3. **Tool Execution**: The agent executes the Python function `search_phones`.
4. **Data Retrieval**: `PhoneDB` filters the JSON list and returns matching phone objects.
5. **Response Generation**: The LLM receives the JSON results and generates a natural language summary with recommendations.

### Comparison Workflow
1. **User Query**: "Compare Pixel 8a and OnePlus 12R"
2. **LLM Analysis**: The model identifies the entities and calls `compare_phones(phone_ids=['pixel_8a', 'oneplus_12r'])`.
3. **Tool Execution**: The agent retrieves full details for both IDs.
4. **Response Generation**: The LLM formats the returned data into a structured Markdown table for easy comparison.

## Tech Stack
- **Language**: Python 3.11+
- **Interface**: Streamlit
- **LLM Provider**: Groq (Model: `openai/gpt-oss-20b`)
- **Data Format**: JSON
- **Dependencies**: `groq`, `python-dotenv`, `streamlit`
