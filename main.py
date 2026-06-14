from brains import ask_gemini, ask_ollama
from tools import ALL_TOOLS
# ── The one line that swaps the brain ──
BACKEND = "gemini"   # "gemini" or "ollama"

BRAINS = {"gemini": ask_gemini, "ollama": ask_ollama}

SYSTEM = "You are a helpful, concise assistant."

def main():
    
    history = []          # neutral format: {"role": "user"/"assistant", "content": ...}
    session_tokens = 0    # running total across the whole conversation

    # Choose brain according to backend
    brain = BRAINS[BACKEND]

    print(f"Chatting with backend: {BACKEND}")
    print("Commands: /reset  /quit\n")

    while True:
        user_input = input("you> ").strip()

        if user_input == "/quit":
            break
        if user_input == "/reset":
            history = []
            print("[history cleared]\n")
            continue
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        reply, usage = ask_gemini(history, SYSTEM, tools=ALL_TOOLS)

        history.append({"role": "assistant", "content": reply})
        session_tokens += usage["total"]

        print(f"\nbot> {reply}")
        print(
            f"[turn: prompt {usage['prompt']} + output {usage['output']} "
            f"= total {usage['total']} | session so far: {session_tokens}]\n"
        )


if __name__ == "__main__":
    main()
