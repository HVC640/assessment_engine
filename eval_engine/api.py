import traceback
from .graph import stream_graph_updates
from .utils import parse_json_response
from core.prompts import EVALUATE_RESPONSE_PROMPT, FEEDBACK_PROMPT
from fastapi import HTTPException, status


def evaluate_response(question: str, answer: str, thread_id: str) -> str:
    config = {"configurable": {"thread_id": thread_id}}
    seed_prompt = EVALUATE_RESPONSE_PROMPT.format(question=question, answer=answer)
    try:
        user_input = f"User: {seed_prompt}"
        response = stream_graph_updates(user_input, config)
        evaluation = parse_json_response(response)
        if evaluation is None:
            raise ValueError("Failed to parse evaluation response as JSON.")
        return evaluation
    except Exception as e:
        error_msg = f"Evaluation failed: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )


def ask_session_question(question: str, thread_id: str) -> str:
    config = {"configurable": {"thread_id": thread_id}}
    seed_prompt = question
    try:
        user_input = f"User: {seed_prompt}"
        response = stream_graph_updates(user_input, config)
        if not response:
            raise ValueError("No response generated for session question.")
        return response
    except Exception as e:
        error_msg = f"Session question failed: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )


def generate_feedback(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    seed_prompt = FEEDBACK_PROMPT
    try:
        user_input = f"User: {seed_prompt}"
        response = stream_graph_updates(user_input, config)
        feedback = parse_json_response(response)
        if feedback is None:
            raise ValueError("Failed to parse feedback response as JSON.")
        return feedback
    except Exception as e:
        error_msg = f"Feedback generation failed: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )


# --- Placeholders for Future Features ---
def generate_followup_question():
    ...


def generate_question_evaluation_report():
    ...


def generate_small_talk():
    ...


def generate_intoduction():
    ...
