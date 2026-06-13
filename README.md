# CLI Chatbot

Terminal chatbot that can talk to either Gemini or a local Ollama model.

## Overview

`main.py` is the interactive chat loop. It keeps conversation history in memory, supports `/reset` and `/quit`, and routes each prompt through the backend selected in `BACKEND`.

`brains.py` holds the model adapters:

- `ask_gemini(...)` sends the chat history to Gemini using `google-genai`
- `ask_ollama(...)` sends the same history to a local Ollama model

The current default backend is Gemini, but you can switch to Ollama by changing `BACKEND` in [main.py](main.py).

## Requirements

- Python 3.14+
- `uv`
- For Gemini: a `GEMINI_API_KEY` environment variable
- For Ollama: a local Ollama installation with the `qwen3:8b` model available

## Setup

Install dependencies from the project folder:

```bash
uv sync
```

If you want to use Gemini, set your API key in the terminal first.

PowerShell:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

cmd.exe:

```bat
set GEMINI_API_KEY=your-api-key
```

If you want to use Ollama, make sure the Ollama service is running and that the model is installed:

```bash
ollama pull qwen3:8b
```

## Run

Start the chatbot with:

```bash
uv run python main.py
```

Edit `BACKEND` in [main.py](main.py) to switch between `gemini` and `ollama`.

## Usage

- Type a message and press Enter to chat.
- Use `/reset` to clear the conversation history.
- Use `/quit` to exit.

## Project Layout

- [main.py](main.py) - interactive CLI chat loop
- [brains.py](brains.py) - Gemini and Ollama backend adapters
- [pyproject.toml](pyproject.toml) - project metadata and dependencies
- [README.md](README.md) - project setup and usage

## Notes

The Gemini path uses `gemini-2.5-flash`, and both backends share the same neutral message format so the chat loop stays simple.
