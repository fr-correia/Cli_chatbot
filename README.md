# CLI Chatbot

Small terminal chatbot built with `google-genai` and Gemini.

## What It Does

`main.py` starts a simple chat loop that sends each user message to Gemini and prints the reply. The conversation history is kept in memory for the life of the process.

`memory.py` contains the same chat-loop logic in a separate module, including token usage reporting after each response.

`goldfish.py` is a minimal single-turn example that sends one prompt and prints the model response.

## Requirements

- Python 3.14+
- A Gemini API key available as `GEMINI_API_KEY`
- `uv` or another Python package manager

## Setup

Install dependencies from the project folder:

```bash
uv sync
```

Set your API key in the terminal before running the chatbot.

PowerShell:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

cmd.exe:

```bat
set GEMINI_API_KEY=your-api-key
```

## Run

Start the chatbot with:

```bash
uv run python main.py
```

For the token-reporting version:

```bash
uv run python memory.py
```

For the one-shot example:

```bash
uv run python goldfish.py
```

## Usage

- Type a message and press Enter to chat.
- Use `/reset` to clear the conversation history.
- Use `/quit` to exit.

## Project Layout

- `main.py` - basic CLI chatbot
- `memory.py` - chat loop with usage tracking
- `goldfish.py` - one-off prompt example
- `pyproject.toml` - project metadata and dependencies

## Notes

The bot currently uses `gemini-2.5-flash` and a short system instruction so responses stay concise.
