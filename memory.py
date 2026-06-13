from google import genai
from google.genai import types

def new_history():
    return []


def main():

    # "Understanding under the hood"
    client = genai.Client()
    MODEL = "gemini-2.5-flash"
    SYSTEM_INSTRUCTION = "You are a friendly, consice assistant. Keep answers short unless asked for detail."

    # Start fresh
    history = new_history()

    print("Chat Started, Type '/reset' to clear memory. '/quit' to exit. \n")

    while True:
        user_input = input("You: ").strip()

        if user_input == "'/quit'":
            print("Closing chat.")
            break
        elif user_input == "'/reset'":
            history = new_history()
            print("[memory cleared]\n")
            break
        elif not user_input:
            continue

        # Save user response in history
        history.append({"role": "user", "parts": [{"text":user_input}]})

        response = client.models.generate_content(
            model=MODEL,
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )

        print("Answer:", response.text, "\n")

        # Save bot reply in history
        history.append({"role": "model", "parts": [{"text":response.text}]})

        # Token meter - how much did this whole call cost in tokens?
        usage = response.usage_metadata
        thinking = getattr(usage, "thoughts_token_count", 0) or 0
        print(f"[tokens — prompt: {usage.prompt_token_count}, "
                f"reply: {usage.candidates_token_count}, "
                f"thinking: {thinking}, "
                f"total: {usage.total_token_count}]\n")
    
if __name__ == "__main__":
    main()