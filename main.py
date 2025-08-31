from fastapi import FastAPI
from eval_engine import eval_engine
from pydantic import BaseModel

# Create FastAPI instance
app = FastAPI(title="Assessment Engine API", version="1.0.0")

# Basic hello world endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World from Assessment Engine!"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Assessment Engine"}


# Define request model
class EvaluationRequest(BaseModel):
    question: str
    answer: str
    thread_id: str

@app.post("/evaluate_response")  # Changed to POST
def evaluate_response(request: EvaluationRequest):
    evaluation = eval_engine.evaluate_response(request.question, request.answer, request.thread_id)
    return {"status": "success", "evaluation": evaluation}

@app.post("/ask_session_question")  # Changed to POST
def ask_session_question(request: EvaluationRequest):
    response = eval_engine.ask_session_question(request.question, request.thread_id)
    return {"status": "success", "response": response}

@app.post("/generate_feedback")  # Changed to POST
def generate_feedback(request: EvaluationRequest):
    feedback = eval_engine.generate_feedback(request.thread_id)
    return {"status": "success", "feedback": feedback}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
