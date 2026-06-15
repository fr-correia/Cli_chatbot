# agent.py — the orchestrator. Owns the loop, the budget, tool execution, and the trace.
from brains import call_ollama
from tools import BY_NAME

MAX_STEPS = 6   # hard budget guard — the ungraceful stop condition

def run_agent(history, system_instruction, tools=None):
    """Drive one agentic TURN to completion: loop model<->tools until the model
    answers with no tool call, or the step budget runs out.

    Returns (final_answer, usage, trace) where:
      - usage = {prompt, output, total} summed across every model call this turn
      - trace = list of step dicts the REPL can print (option B)
    """
    # The orchestrator owns the message list now. Prepend system, then the history.
    messages = [{"role": "system", "content": system_instruction}]
    messages.extend(history)

    usage = {"prompt": 0, "output": 0, "total": 0}
    trace = []

    for step in range(1, MAX_STEPS + 1):
        msg, u = call_ollama(messages, tools=tools)   # ONE model call
        # accumulate usage correctly: each call's delta added once
        usage["prompt"] += u["prompt"]
        usage["output"] += u["output"]
        usage["total"]  += u["total"]

        messages.append(msg)   # the agent must see its own action next round

        if not msg.tool_calls:                  # DONE — graceful stop
            return msg.content, usage, trace

        for call in msg.tool_calls:             # execute each requested tool
            name = call.function.name
            args = dict(call.function.arguments)
            fn = BY_NAME.get(name)
            if fn is None:
                result = f"ERROR: unknown tool {name}"
            else:
                try:
                    result = fn(**args)
                except Exception as e:
                    result = f"ERROR: {e}"        # e.g. calculate on a bad expression

            trace.append({"step": step, "tool": name, "args": args, "result": str(result)})

            messages.append({
                "role": "user",
                "tool_name": name,
                "content": str(result),
            })

    # Budget guard fired — ungraceful stop
    return "[stopped: hit step budget without finishing]", usage, trace


if __name__ == "__main__":
    hist = [{"role": "user",
             "content": "What's the weather in Basel and Tokyo? Multiply them, then divide by 7."}]
    SYS = ("You are a task-completing agent. You are FORBIDDEN from doing arithmetic "
           "yourself — all math must go through the calculate tool. Answer in plain text when done.")
    from tools import ALL_TOOLS
    answer, usage, trace = run_agent(hist, SYS, tools=ALL_TOOLS)
    print("\nTRACE:")
    for t in trace:
        print(f"  step {t['step']}: {t['tool']}({t['args']}) -> {t['result']}")
    print("\nANSWER:", answer)
    print("USAGE:", usage)