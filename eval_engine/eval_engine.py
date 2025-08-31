#TODO write setup
import json
import os
import traceback
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict
from typing import Annotated

os.environ["TAVILY_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDWPc1-mnhS67XK-oW4P6MrZaFs2xpdRvU"
llm = init_chat_model("google_genai:gemini-2.0-flash")

class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)


def stream_graph_updates(user_input: str, config: dict):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config):
        for value in event.values():
            return value["messages"][-1].content


def parse_json_response(response_str):
    try:
        # Remove markdown code block markers
        cleaned = response_str.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned[7:]  # Remove ```json
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]  # Remove ```
        
        # Remove extra backslashes and fix escaped quotes
        cleaned = cleaned.replace('\\n', '\n')
        cleaned = cleaned.replace('\\"', '"')
        cleaned = cleaned.replace('\\\\', '\\')
        
        # Parse JSON
        result = json.loads(cleaned.strip())
        return result
    
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        print(f"Cleaned string: {repr(cleaned)}")
        return None


# API Endpoints

def evaluate_response(question: str, answer: str, thread_id: str) -> str:
    config = {"configurable": {"thread_id": thread_id}}
    evaluation = ""
    seed_prompt = f"""
    You are a Programming Interviewer. Evaluate the candidate's answer below:

    Question: {question}
    Answer: {answer}

    Provide scores (1-10) for each criterion and return your evaluation in this exact JSON format:

    {{
        "confidence_score": <1-10>,
        "depth_score": <1-10>,
        "accuracy_score": <1-10>,
        "feedback": "Brief explanation of the scores"
    }}

    Scoring Guidelines:
    - confidence_score: How confident and clear the candidate sounds
    - depth_score: How thorough and detailed the explanation is
    - accuracy_score: How technically correct the answer is
    """

    try:
        user_input = f"User: {seed_prompt}"
        response = stream_graph_updates(user_input, config)
        evaluation = parse_json_response(response)
    except Exception as e:
        print("Failed ", e)
        print(traceback.format_exc())

    return evaluation


def ask_session_question(question: str, thread_id: str) -> str:
    config = {"configurable": {"thread_id": thread_id}}
    response = ""
    seed_prompt = question

    try:
        user_input = f"User: {seed_prompt}"
        response = stream_graph_updates(user_input, config)
    except Exception as e:
        print("Failed ", e)
        print(traceback.format_exc())

    return response


    # INTERVIEW DATA:
    # - Total Questions Asked: {total_questions}
    # - Individual Question Scores: {question_scores}
    # - Overall Performance Summary: {performance_summary}


def generate_feedback(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    feedback = ""
    seed_prompt = """
    You are an experienced Programming Interview Assessor. You have conducted a complete interview session with a candidate and now need to provide a comprehensive overall assessment.

    TASK:
    Generate a comprehensive overall feedback report that synthesizes the candidate's performance across all questions asked during the interview.

    RESPONSE FORMAT:
    Provide your assessment in the following JSON format:

    {{
        "overall_score": <score out of 10>,
        "technical_competency": "<Beginner/Intermediate/Advanced>",
        "strengths": [
            "strength 1",
            "strength 2",
            "strength 3"
        ],
        "areas_for_improvement": [
            "area 1",
            "area 2", 
            "area 3"
        ],
        "interview_performance": {{
            "communication_clarity": <score out of 10>,
            "problem_solving_approach": <score out of 10>,
            "technical_accuracy": <score out of 10>,
            "confidence_level": <score out of 10>
        }},
        "hiring_recommendation": "<Strong Hire/Hire/Borderline/No Hire>",
        "detailed_feedback": "Comprehensive 3-4 sentence summary of the candidate's overall performance, highlighting key observations and justifying the hiring recommendation",
        "next_steps": "Specific recommendations for the candidate's development or next interview rounds"
    }}

    EVALUATION CRITERIA:
    - Consider consistency across all questions
    - Look for patterns in strengths and weaknesses
    - Assess growth/learning during the interview
    - Evaluate technical depth vs breadth of knowledge
    - Consider communication skills and thought process
    - Factor in the difficulty level of questions asked

    SCORING GUIDELINES:
    - Overall Score: Weighted average considering question difficulty and performance trends
    - Technical Competency: Based on depth of answers and problem-solving approach
    - Individual Performance Metrics: Rate 1-10 based on observed behaviors
    - Hiring Recommendation: Align with company standards and role requirements

    Be objective, constructive, and provide actionable insights for both the candidate and hiring team.
    """

    try:
        user_input = f"User: {seed_prompt}"
        response = stream_graph_updates(user_input, config)
        feedback = parse_json_response(response)
    except Exception as e:
        print("Failed ", e)
        print(traceback.format_exc())

    return feedback


def generate_followup_question():
    ...


def generate_question_evaluation_report():
    ...


def generate_small_talk():
    ...


def generate_intoduction():
    ...
