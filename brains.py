from google import genai
from google.genai import types
from ollama import chat
from tools import BY_NAME

# Gemini client initialization
gemini_client = genai.Client()

def ask_gemini(history, system_instruction, tools=None):
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

def ask_ollama(history, system_instruction, tools=None):
    # Neutral history is ALREADY in Ollama's shape — just prepend the system turn.
    messages = [{"role": "system", "content": system_instruction}]
    messages.extend(history)

    usage = {"prompt": 0, "output": 0, "total": 0}

    for _ in range(5):
        response = chat(model="qwen3:8b", messages=messages, tools=tools,think=False)
        usage["prompt"] += response.prompt_eval_count
        usage["output"] += response.eval_count
        usage["total"] += usage["prompt"]+usage["output"]

        messages.append(response.message)

        if response.message.tool_calls:
            for call in response.message.tool_calls:
                fn = BY_NAME.get(call.function.name)
                args = call.function.arguments
                result = fn(**args) if fn else f"no tool named {call.function.name}"
                messages.append({
                    "role": "user",
                    "tool_name": call.function.name,
                    "content": str(result)
                })
            continue

        return response.message.content, usage

    return "[stopped: too many tool steps]", usage

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