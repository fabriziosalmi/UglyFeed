from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
import logging
import os

app = FastAPI()

# Configuration
# this proxy convert ollama api requests into OpenAI api requests (wider audience and tools)
# proxy will run on port 8028 then just update llm_processor.py LLM API port to 8028 and you are done!
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "http://localhost:11434/v1/chat/completions")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define request and response models
class OllamaRequest(BaseModel):
    prompt: str

class OpenAIMessage(BaseModel):
    role: str
    content: str

class OpenAIRequest(BaseModel):
    model: str
    messages: list[OpenAIMessage]

class OpenAIResponseChoice(BaseModel):
    message: OpenAIMessage

class OpenAIResponse(BaseModel):
    id: str
    model: str
    created: int
    choices: list[OpenAIResponseChoice]

class OllamaResponse(BaseModel):
    id: str
    model: str
    created: int
    response: str

@app.post("/api/chat", response_model=OllamaResponse)
async def proxy_ollama_to_openai(ollama_request: OllamaRequest):
    try:
        # Transform Ollama request to OpenAI format
        openai_request = OpenAIRequest(
            model="phi3",
            messages=[
                OpenAIMessage(role="user", content=ollama_request.prompt)
            ]
        )

        # Send the transformed request to OpenAI API
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENAI_API_URL, json=openai_request.dict())
            response.raise_for_status()

        # Transform OpenAI response back to Ollama format
        openai_response = OpenAIResponse(**response.json())
        ollama_response = OllamaResponse(
            id=openai_response.id,
            model=openai_response.model,
            created=openai_response.created,
            response=openai_response.choices[0].message.content
        )

        return ollama_response

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error communicating with OpenAI API: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8028)