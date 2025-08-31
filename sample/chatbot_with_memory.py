from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

import os

os.environ["TAVILY_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDWPc1-mnhS67XK-oW4P6MrZaFs2xpdRvU"
llm = init_chat_model("google_genai:gemini-2.0-flash")


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

tool = TavilySearch(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}


def stream_graph_updates(user_input: str):
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    ):
        event["messages"][-1].pretty_print()


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except Exception:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break

"""
You are a reviewer, you have to evaulate the following programming answer based on the question, 'question': 'What is python', 'answer': 'Python is a snake'. Based on the answer give a rating out of 5. Below are the parameter you have to judge on parms: 'does answer explain OOPs, inhertiance ? NOTE: Give your response in a json format with follwing key values ['rating', 'follow_up_question', 'precision', 'reason_for_rating']

{
  "rating": 1,
  "follow_up_question": "Could you please provide a definition of Python in the context of computer science, and explain its object-oriented programming features, including inheritance?",
  "precision": "The answer is factually correct that a python is a snake, but completely irrelevant and incorrect in the context of the question about the Python programming language.",
  "reason_for_rating": "The answer demonstrates a complete misunderstanding of the question. It provides a definition of 'python' as a reptile, rather than the Python programming language. It fails to address any of the requested aspects, such as OOPs or inheritance, making it a highly inappropriate and unhelpful response."
}

"""

"""
You are a reviewer, you have to evaulate the following anser based on the question, 'question': 'What is AWS', 'answer': 'AWS stands for Amazon Web Service'. Based on the answer give a rating out of 5. Below are the parameter you have to judge on parms: 'Does answer explain AWS, Functions, S3 ? NOTE: Give your response in a json format with follwing key values ['rating', 'follow_up_question', 'precision', 'reason_for_rating']
"""

{
    "rating": 2,
    "follow_up_question": "Could you elaborate on what kind of programming language Java is, mentioning its key features like object-oriented programming (OOP) and inheritance?",
    "precision": "Low",
    "reason_for_rating": "The answer is factually correct but provides a very basic and incomplete definition of Java. It lacks depth and doesn't mention important aspects like object-oriented programming (OOP) or inheritance, which are fundamental to understanding Java.",
}
{
    "rating": 1,
    "follow_up_question": "Can you elaborate on what Amazon Web Services (AWS) is and provide some examples of its services?",
    "precision": "Low",
    "reason_for_rating": "The answer only provides the acronym's full form. It doesn't explain what AWS *is*, its functions, or any specific services like S3. It lacks any meaningful information about the cloud platform itself.",
}

"""
Okay, I understand. Based on the previous two evaluations, here's some overall feedback and a final rating:

**Feedback:**

The model struggles to provide comprehensive answers, especially when the prompt expects explanations of specific features or functionalities. The answers tend to be very basic and often only scratch the surface of the topic. The model needs to be improved to provide more detailed and informative responses that address all aspects of the question. It should also be able to understand and incorporate specific requirements mentioned in the prompt (e.g., explaining OOPs concepts or specific AWS services).

**Final Rating:**

2/5
"""

"""
The questions asked, were they interlinked to eachother ?, If yes then why ?

No, the questions "What is Java?" and "What is AWS?" are not directly interlinked. They are independent questions about different topics:

*   **"What is Java?"** is a question about a programming language.
*   **"What is AWS?"** is a question about a cloud computing platform.

There's no inherent connection between the two; understanding one doesn't necessarily require knowledge of the other. They are separate topics within the broader fields of software development and cloud computing.
"""
