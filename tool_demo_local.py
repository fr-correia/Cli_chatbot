from ollama import chat

# 1. A real function. The docstring IS the schema the model reads — be precise.
def get_weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: The name of the city to get the weather for.

    """

    fake_db = {"Basel": "12°C, light rain", "Tokyo": "24°C, clear"}
    return fake_db.get(city, "no data for that city")


def main():
    
    messages = [{"role": "user", "content": "What's the weather in Basel right now?"}]

    # --- CALL: pass the function straight in; the SDK builds the schema from it ---
    resp = chat(model="qwen3:8b", messages=messages, tools=[get_weather], think=False)

    # Ollama puts the model's turn (which may contain tool calls) on resp.message
    messages.append(resp.message)  # keep the assistant's tool-call turn in history

    if resp.message.tool_calls:
        call = resp.message.tool_calls[0]
        print(f"[model wants to call] {call.function.name}({dict(call.function.arguments)})")

        # --- TOOL: you run the real function ---
        result = get_weather(**call.function.arguments)
        print(f"[tool returned] {result}")

        # --- RESULT: a dedicated 'tool' role message, tagged with the tool's name ---
        messages.append({
            "role": "tool",
            "tool_name": call.function.name,
            "content": str(result),
        })

        # --- ANSWER: second round-trip, now grounded ---
        final = chat(model="qwen3:8b", messages=messages, think=False)
        print(f"[final answer] {final.message.content}")
    else:
        print(f"[no tool needed] {resp.message.content}")

if __name__ == "__main__":
    main()
