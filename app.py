from fastapi import FastAPI
from eval_engine import api
from core.schemas import (
    EvaluateResponseRequest,
    AskSessionQuestionRequest,
    GenerateFeedbackRequest,
)

app = FastAPI(title="Assessment Engine API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello World from Assessment Engine!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Assessment Engine"}

@app.post("/evaluate_response")
def evaluate_response(request: EvaluateResponseRequest):
    evaluation = api.evaluate_response(
        request.question, request.answer, request.thread_id
    )
    return {"status": "success", "evaluation": evaluation}

@app.post("/ask_session_question")
def ask_session_question(request: AskSessionQuestionRequest):
    response = api.ask_session_question(
        request.question, request.thread_id
    )
    return {"status": "success", "response": response}

@app.post("/generate_feedback")
def generate_feedback(request: GenerateFeedbackRequest):
    feedback = api.generate_feedback(request.thread_id)
    return {"status": "success", "feedback": feedback}