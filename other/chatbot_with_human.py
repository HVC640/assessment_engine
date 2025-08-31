from typing import Annotated

from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt

import os
from langchain.chat_models import init_chat_model

os.environ["TAVILY_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDWPc1-mnhS67XK-oW4P6MrZaFs2xpdRvU"
llm = init_chat_model("google_genai:gemini-2.0-flash")

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]

tool = TavilySearch(max_results=2)
tools = [tool, human_assistance]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    assert(len(message.tool_calls) <= 1)
    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory, interrupt_before=["tools"])

config = {"configurable": {"thread_id": "1"}}

def stream_graph_updates(user_input: str):
    events = list(graph.stream({"messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"))
    
    # Check if we're interrupted (waiting for human input)
    snapshot = graph.get_state(config)
    
    # If we're at an interrupt point, handle it
    while snapshot.next:
        # Check if we need human assistance
        if "tools" in snapshot.next:
            # Get the last message to see if it's asking for human assistance
            last_message = snapshot.values["messages"][-1]
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                for tool_call in last_message.tool_calls:
                    if tool_call["name"] == "human_assistance":
                        # Extract the query from the tool call
                        query = tool_call["args"]["query"]
                        print(f"\n🤖 AI is requesting human assistance:")
                        print(f"Query: {query}")
                        
                        # Get human response
                        human_response = input("Human Expert: ")
                        
                        # Resume with human response
                        human_command = Command(resume={"data": human_response})
                        events = list(graph.stream(human_command, config, stream_mode="values"))
                        
                        # Update snapshot
                        snapshot = graph.get_state(config)
                        break
            else:
                # If it's not human assistance, just continue
                events = list(graph.stream(None, config, stream_mode="values"))
                snapshot = graph.get_state(config)
        else:
            break
    
    # Print the final messages
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()

def run_conversation():
    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break

# Start the conversation
if __name__ == "__main__":
    print("🤖 AI Assistant with Human-in-the-Loop is ready!")
    print("The AI can request human assistance when needed.")
    print("Type 'quit', 'exit', or 'q' to end the conversation.\n")
    run_conversation()
