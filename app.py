from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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
    try:
        evaluation = api.evaluate_response(
            request.question, request.answer, request.thread_id
        )
        return JSONResponse(content={"status": "success", "evaluation": evaluation})
    except HTTPException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "detail": exc.detail},
        )


@app.post("/ask_session_question")
def ask_session_question(request: AskSessionQuestionRequest):
    try:
        response = api.ask_session_question(request.question, request.thread_id)
        return JSONResponse(content={"status": "success", "response": response})
    except HTTPException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "detail": exc.detail},
        )


@app.post("/generate_feedback")
def generate_feedback(request: GenerateFeedbackRequest):
    try:
        feedback = api.generate_feedback(request.thread_id)
        return JSONResponse(content={"status": "success", "feedback": feedback})
    except HTTPException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "detail": exc.detail},
        )
