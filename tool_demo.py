from google import genai
from google.genai import types

# 1. A real function. The docstring IS the schema the model reads — be precise.
def get_weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: The name of the city to get the weather for.

    """

    fake_db = {"Basel": "12°C, light rain", "Tokyo": "24°C, clear"}
    return fake_db.get(city, "no data for that city")


def main():
    client = genai.Client()

    # 2. Tell the model the tool exists, but DISABLE auto-execution so WE drive the loop.
    config = types.GenerateContentConfig(
        tools=[get_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
    contents = [
        types.Content(role="user", parts=[types.Part(text="What's the weather in Basel right now?")])
    ]

    # --- CALL: first round-trip ---
    resp = client.models.generate_content(
        model="gemini-2.5-flash", contents=contents, config=config
    )

    if resp.function_calls:
        fc = resp.function_calls[0]
        print(f"[model wants to call] {fc.name}({dict(fc.args)})")

        # --- TOOL: you run the real function ---
        result = get_weather(**fc.args)
        print(f"[tool returned] {result}")

        # --- RESULT: append the model's request turn + your function's answer ---
        contents.append(resp.candidates[0].content)  # the model's tool-call turn
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_function_response(
                name=fc.name, response={"result": result}
            )],
        ))

        # --- ANSWER: second round-trip, now grounded in the result ---
        final = client.models.generate_content(
            model="gemini-2.5-flash", contents=contents, config=config
        )
        print(f"[final answer] {final.text}")
    else:
        print(f"[no tool needed] {resp.text}")

if __name__ == "__main__":
    main()
