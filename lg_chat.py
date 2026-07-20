from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from brains import call_ollama  # adjust to wherever it actually lives

class State(TypedDict):
    messages: list
    usage: list

def call_model(state: State) -> dict:
    response, usage = call_ollama(state["messages"])
    return {
        "messages": state["messages"] + [response],
        "usage": state.get("usage", []) + [usage],
    }

graph = StateGraph(State)
graph.add_node("call_model", call_model)
graph.add_edge(START, "call_model")
graph.add_edge("call_model", END)

app = graph.compile()
result = app.invoke({
    "messages": [{"role": "user", "content": "Say hello in one sentence."}],
    "usage": [],
})
for m in result["messages"]:
    print(m)
print(result["usage"])