from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    count: int

def increment(state: State) -> dict:
    print(f"in node, count is {state['count']}")
    return {"count": state["count"] + 1}

def should_continue(state: State) -> str:
    return "loop" if state["count"] < 3 else "done"

graph = StateGraph(State)
graph.add_node("increment", increment)
graph.add_edge(START, "increment")
graph.add_conditional_edges(
    "increment",
    should_continue,
    {"loop": "increment", "done": END},
)

app = graph.compile()
result = app.invoke({"count": 0})
print(result)