import ollama
from tools import ALL_TOOLS, BY_NAME

MODEL = "qwen3:8b"
MAX_STEPS = 6 # Hard budget: An agent without a cap can loop forever

def run_agent(goal: str):
    messages = [
        {
            "role": "system",
            "content": "You are a task-completing agent. Use the available tools to reach the user's goal. "
                        "You are FORBIDDEN from doing any arithmetic yourself — even simple sums. "
                        "ALL math, without exception, must go through the calculate tool. "
                        "When you have the final answer, reply in plain text with no tool call."
        },
        {
            "role": "user",
            "content": goal
        }
    ]
    print(f"Goal: {goal}\n")

    for step in range( MAX_STEPS):
        resp = ollama.chat(model=MODEL, messages=messages, tools=ALL_TOOLS, think=False)
        msg = resp.message
        messages.append(msg)

        if not msg.tool_calls:
            print(f"\n[Step {step}] DONE")
            print("Answer:", msg.content)
            return msg.content

        for call in msg.tool_calls:
            name = call.function.name
            args = dict(call.function.arguments)

            fn = BY_NAME.get(name)

            try:
                result = fn(**args)
            except Exception as e:
                result = f"ERROR: {e}"
            print(f"[STEP {step}] OBSERVATION: {result}")

            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": str(result)
            })
    print(f"\n[!] Hit MAX_STEPS ({MAX_STEPS}) without finishing - budget guard fired")
    return None

if __name__ == "__main__":
    run_agent("What's the weather in Basel and Tokyo? Multiply the two temperatures together, then divide by 7.")