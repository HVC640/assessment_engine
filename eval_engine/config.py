import os
from langchain.chat_models import init_chat_model

# --- Environment Setup ---
os.environ["TAVILY_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDWPc1-mnhS67XK-oW4P6MrZaFs2xpdRvU"

llm = init_chat_model("google_genai:gemini-2.0-flash")
