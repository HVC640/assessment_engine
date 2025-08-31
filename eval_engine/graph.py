from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict
from typing import Annotated
from .config import llm

# --- State Definition ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- Graph Setup ---
graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)

def stream_graph_updates(user_input: str, config: dict):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config):
        for value in event.values():
            return value["messages"][-1].content