from fastapi import FastAPI
from pydantic import BaseModel
from eval_engine import eval_engine
import uvicorn

app = FastAPI(title="Assessment Engine API", version="1.0.0")

# --- Request Models ---

class EvaluateResponseRequest(BaseModel):
    question: str
    answer: str
    thread_id: str

class AskSessionQuestionRequest(BaseModel):
    question: str
    thread_id: str

class GenerateFeedbackRequest(BaseModel):
    thread_id: str

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Hello World from Assessment Engine!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Assessment Engine"}

@app.post("/evaluate_response")
def evaluate_response(request: EvaluateResponseRequest):
    evaluation = eval_engine.evaluate_response(
        request.question, request.answer, request.thread_id
    )
    return {"status": "success", "evaluation": evaluation}

@app.post("/ask_session_question")
def ask_session_question(request: AskSessionQuestionRequest):
    response = eval_engine.ask_session_question(
        request.question, request.thread_id
    )
    return {"status": "success", "response": response}

@app.post("/generate_feedback")
def generate_feedback(request: GenerateFeedbackRequest):
    feedback = eval_engine.generate_feedback(request.thread_id)
    return {"status": "success", "feedback": feedback}

if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8000)
