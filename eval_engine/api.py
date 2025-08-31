import traceback
from .graph import stream_graph_updates
from .utils import parse_json_response
from core.prompts import EVALUATE_RESPONSE_PROMPT, FEEDBACK_PROMPT


def evaluate_response(question: str, answer: str, thread_id: str) -> str:
    config = {"configurable": {"thread_id": thread_id}}
    evaluation = ""
    seed_prompt = EVALUATE_RESPONSE_PROMPT.format(question=question, answer=answer)
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


def generate_feedback(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    feedback = ""
    seed_prompt = FEEDBACK_PROMPT
    try:
        user_input = f"User: {seed_prompt}"
        response = stream_graph_updates(user_input, config)
        feedback = parse_json_response(response)
    except Exception as e:
        print("Failed ", e)
        print(traceback.format_exc())
    return feedback


# --- Placeholders for Future Features ---
def generate_followup_question(): ...


def generate_question_evaluation_report(): ...


def generate_small_talk(): ...


def generate_intoduction(): ...
