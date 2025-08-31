# Assessment Engine

## Overview

The main objective of this project is to provide an intelligent AI bot that conducts interviews. The interview process is controlled by an external bot or system, which interacts with this engine via API calls.

## Features

- **Automated Interviewing:** The AI bot can ask questions, evaluate responses, and generate feedback.
- **API Driven:** All interactions are exposed as RESTful APIs for easy integration with external systems.
- **Modular Design:** Codebase is organized for maintainability and scalability, with clear separation of prompts, schemas, and business logic.

## Project Structure

```
assessment_engine/
│
├── app.py                # FastAPI application and endpoints
├── main.py               # Entry point to run the server
├── core/
│   ├── prompts.py        # Prompt templates for the AI
│   └── schemas.py        # Pydantic models for request validation
├── eval_engine/
│   ├── api.py            # Core API logic for evaluation and feedback
│   ├── config.py         # Model and environment configuration
│   ├── graph.py          # LangGraph setup and streaming logic
│   └── utils.py          # Utility functions
└── README.md             # Project documentation
```

## Getting Started

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the server:**
    ```bash
    python main.py
    ```

3. **API Endpoints:**
    - `POST /evaluate_response`
    - `POST /ask_session_question`
    - `POST /generate_feedback`

## Usage

Integrate with your external bot or system by making HTTP requests to the provided endpoints. Refer to the `core/schemas.py` for request payload formats.

## License