import traceback
from .graph import stream_graph_updates
from .utils import parse_json_response
from core.prompts import EVALUATE_RESPONSE_PROMPT, FEEDBACK_PROMPT, INTRODUCTION_PROMPT
from fastapi import HTTPException, status


# --- Core Evaluation Engine Functions ---
def evaluate_response(question: str, answer: str, thread_id: str) -> str:
    """
    Evaluates a user's answer to a given question within a specific thread context.

    Args:
        question (str): The question to be evaluated.
        answer (str): The user's answer to the question.
        thread_id (str): The identifier for the thread in which the evaluation is taking place.

    Returns:
        str: The evaluation result parsed from the response, typically in JSON format.

    Raises:
        HTTPException: If the evaluation fails or the response cannot be parsed as JSON.
    """
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
    """
    Asks a session-specific question and returns the generated response.

    Args:
        question (str): The question to be asked in the session.
        thread_id (str): The identifier for the session thread.

    Returns:
        str: The generated response to the session question.

    Raises:
        HTTPException: If no response is generated or an error occurs during processing.
    """
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


def generate_feedback(thread_id: str) -> dict:
    """
    Generates feedback for a given thread by invoking a feedback prompt and processing the response.

    Args:
        thread_id (str): The unique identifier of the thread for which feedback is to be generated.

    Returns:
        dict: The parsed feedback response as a dictionary.

    Raises:
        HTTPException: If feedback generation fails or the response cannot be parsed as JSON.
    """
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


def generate_intoduction(
    thread_id: str, resume: str = None, job_description: str = None
) -> str:
    """
    Generates an introduction prompt for an interviewee based on provided context.
    Args:
        thread_id (str): Unique identifier for the interview thread.
        resume (str, optional): Candidate's resume text to personalize the introduction prompt. Defaults to None.
        job_description (str, optional): Job description text to further tailor the prompt. Defaults to None.
    Returns:
        str: The generated introduction prompt or question for the candidate.
    Raises:
        HTTPException: If prompt generation fails or no introduction question is generated.
    Behavior:
        - If only thread_id is provided, generates a generic introduction question.
        - If resume and/or job_description are provided, incorporates them into the prompt for a more personalized introduction.
    """
    config = {"configurable": {"thread_id": thread_id}}

    # Prepare dynamic context for the prompt
    context_parts = []
    if resume:
        context_parts.append(f"Resume:\n{resume}")
    if job_description:
        context_parts.append(f"Job Description:\n{job_description}")

    context = "\n\n".join(context_parts) if context_parts else None

    # Format the prompt with or without context
    if context:
        seed_prompt = INTRODUCTION_PROMPT.format(context=context)
    else:
        # If no context, provide a generic introduction instruction
        seed_prompt = INTRODUCTION_PROMPT.format(
            context="Please ask the candidate a generic introduction question such as: 'Can you please introduce yourself and tell me about your background?'"
        )

    try:
        user_input = f"User: {seed_prompt}"
        response = stream_graph_updates(user_input, config)
        if not response:
            raise ValueError("No introduction question generated.")
        return response
    except Exception as e:
        error_msg = f"Introduction prompt generation failed: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )


# --- Placeholders for Future Features ---
def generate_followup_question(): ...


def generate_question_evaluation_report(): ...


def generate_small_talk(): ...
