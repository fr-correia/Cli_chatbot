from typing import Literal
from pydantic import BaseModel

class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative', 'neutral']
    summary: str
    topics: list[str]

TEXT = (
    "Honestly the new dark mode looks great, but the app crashes every time"
    "I open settings on my old phone. Fix that and it´s perfect!"
)

# Gemini
from google import genai
from google.genai import types

client = genai.Client()
gemini_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"Classify this user feedback:\n\n{TEXT}",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",  # emite json
        response_schema=Feedback                # json matching this shape
    )
)

gemini_fb = gemini_response.parsed  # already parsed into a Feedback object
print("Gemini response:", gemini_fb)

# Ollama
from ollama import chat

ollama_response = chat(
    model="qwen3:8b",
    messages=[{"role": "user", "content": f"Classify this user feedback:\n\n{TEXT}"}],
    format=Feedback.model_json_schema(),  # emite json matching the Feedback schema
    think=False,
    options={"temperature": 0}  # deterministic output -> Schema validation is more likely to succeed
)

ollama_fb = Feedback.model_validate_json(ollama_response.message.content)  # parse the json into a Feedback object
print("Ollama response:", ollama_fb)