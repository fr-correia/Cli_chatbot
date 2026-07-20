from google import genai
from google.genai import types
from ollama import chat
from tools import BY_NAME



def ask_gemini(history, system_instruction, tools=None):
    # Gemini client initialization
    gemini_client = genai.Client()
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

    usage = {"prompt": 0, "output": 0, "total": 0}

    for _ in range(5):
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
            ),
        )
        um = response.usage_metadata
        usage["prompt"] += um.prompt_token_count
        usage["output"] += um.candidates_token_count
        usage["total"] += um.total_token_count

        if response.function_calls:
            contents.append(response.candidates[0].content)  # the model's tool-call turn
            for fc in response.function_calls:
                fn = BY_NAME[fc.name]
                result = fn(**fc.args) if fn else f"no tool named {fc.name}"
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(
                        name=fc.name, response={"result": result}
                    )],
                ))
            continue

        return response.text, usage


    return "[stopped: too many tool steps]", usage

def call_ollama(messages, tools=None):
    """ONE model call. No loop, no tool execution. The orchestrator owns those.
    `messages` arrives already in Ollama's shape (system turn included).
    Returns (response_message, usage_dict)."""
    response = chat(model="qwen3:8b", messages=messages, tools=tools, think=False)
    usage = {
        "prompt": response.prompt_eval_count,
        "output": response.eval_count,
        "total": response.prompt_eval_count + response.eval_count,
    }
    return response.message, usage

if __name__ == "__main__":
    SYSTEM = "You are a terse assistant. Answer in exactly one sentence."
    history = [{"role": "user", "content": "What is VRAM, briefly?"}]

    print("--- Gemini (cloud) ---")
    text, usage = ask_gemini(history, SYSTEM)
    print(text)
    print(usage)

    print("\n--- Ollama (local) ---")
    text, usage = call_ollama(history, SYSTEM)
    print(text)
    print(usage)