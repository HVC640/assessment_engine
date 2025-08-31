from pydantic import BaseModel


class EvaluateResponseRequest(BaseModel):
    question: str
    answer: str
    thread_id: str


class AskSessionQuestionRequest(BaseModel):
    question: str
    thread_id: str


class GenerateFeedbackRequest(BaseModel):
    thread_id: str
