from tools import ALL_TOOLS
from agent import run_agent
# ── The one line that swaps the brain ──
BACKEND = "ollama"   # "gemini" or "ollama"

SYSTEM = "You are a helpful, concise assistant."

SHOW_TRACE = True    # print the agent's actions live+

def main():
    
    history = []          # neutral format: {"role": "user"/"assistant", "content": ...}
    session_tokens = 0    # running total across the whole conversation

    print(f"Chatting with backend: {BACKEND}")
    print("Commands: /reset  /quit  /trace (toggle agent trace)\n")

    global SHOW_TRACE

    while True:
        user_input = input("you> ").strip()

        if user_input == "/quit":
            break
        if user_input == "/reset":
            history = []
            print("[history cleared]\n")
            continue
        if user_input == "/trace":
            SHOW_TRACE = not SHOW_TRACE
            print(f"[trace: {'ON' if SHOW_TRACE else 'OFF'}]\n")
            continue
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        reply, usage, trace = run_agent(history, SYSTEM, tools=ALL_TOOLS)

        # option B: show what the agent actually did, before the answer
        if SHOW_TRACE and trace:
            print("\n[agent trace]")
            for t in trace:
                print(f"  step {t['step']}: {t['tool']}({t['args']}) -> {t['result']}")

        history.append({"role": "assistant", "content": reply})
        session_tokens += usage["total"]

        print(f"\nbot> {reply}")
        print(
            f"[turn: prompt {usage['prompt']} + output {usage['output']} "
            f"= total {usage['total']} | session so far: {session_tokens}]\n"
        )


if __name__ == "__main__":
    main()
