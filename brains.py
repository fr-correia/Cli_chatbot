from google import genai
from google.genai import types
from ollama import chat

# Gemini client initialization
gemini_client = genai.Client()

def ask_gemini(history, system_instruction):
    # $env:GEMINI_API_KEY="API_KEY"
    # Translate neutral -> gemini shape: "assistant" becomes "model",
    # and "content" becomes a "parts" list:
    contents = [
        {
            "role": "model" if turn["role"] == "assistant" else "user",
            "parts": [{"text": turn["content"]}],
        }
        for turn in history
    ]

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        ),
    )
    usage = {
        "prompt": response.usage_metadata.prompt_token_count,
        "output": response.usage_metadata.candidates_token_count,
        "total": response.usage_metadata.total_token_count,
    }
    return response.text, usage

def ask_ollama(history, system_instruction):
    # Neutral history is ALREADY in Ollama's shape — just prepend the system turn.
    messages = [{"role": "system", "content": system_instruction}]
    messages.extend(history)
    response = chat(model="qwen3:8b", messages=messages, think=False)
    usage = {
        "prompt": response.prompt_eval_count,
        "output": response.eval_count,
        "total": (response.prompt_eval_count or 0) + (response.eval_count or 0),
    }
    return response.message.content, usage

if __name__ == "__main__":
    SYSTEM = "You are a terse assistant. Answer in exactly one sentence."
    history = [{"role": "user", "content": "What is VRAM, briefly?"}]

    print("--- Gemini (cloud) ---")
    text, usage = ask_gemini(history, SYSTEM)
    print(text)
    print(usage)

    print("\n--- Ollama (local) ---")
    text, usage = ask_ollama(history, SYSTEM)
    print(text)
    print(usage)