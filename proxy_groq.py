from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import logging
import json

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configuration for local OpenAI API @ Groq
OPENAI_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

@app.post('/api/chat')
async def chat_completions(request: Request):
    try:
        # Capture the request data from the client
        ollama_data = await request.json()
        logging.info(f"Received Ollama API request: {json.dumps(ollama_data, indent=2)}")

        # Transform Ollama API request to OpenAI API @ Groq request
        openai_request_data = transform_ollama_to_openai(ollama_data)
        logging.info(f"Transformed OpenAI API request: {json.dumps(openai_request_data, indent=2)}")

        # Forward the transformed request to OpenAI API @ Groq
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(OPENAI_API_URL, headers=headers, json=openai_request_data)

        # Check for HTTP errors
        response.raise_for_status()

        # Transform the OpenAI API response @ Groq to Ollama API response format
        openai_response_data = response.json()
        logging.info(f"Received OpenAI API response: {json.dumps(openai_response_data, indent=2)}")
        transformed_response_data = transform_openai_to_ollama(openai_response_data)
        logging.info(f"Transformed Ollama API response: {json.dumps(transformed_response_data, indent=2)}")

        # Send the transformed response back to the client
        return JSONResponse(content=transformed_response_data)

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    except Exception as e:
        logging.error(f"Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)

def transform_ollama_to_openai(ollama_data):
    messages = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in ollama_data.get("messages", [])
    ]

    return {
        "model": ollama_data.get("model", "llama3-70b-8192"),
        "messages": messages,
        "temperature": 0,
        "max_tokens": 4096
    }

# available models @ Groq:
# Mixtral-8x7b-32768
# llama3-70b-8192
# llama3-8b-8192
# Gemma-7b-It

def transform_openai_to_ollama(openai_data):
    choices = openai_data.get("choices", [])
    if choices:
        first_choice = choices[0]
        message = {
            "role": first_choice.get("message", {}).get("role", "assistant"),
            "content": first_choice.get("message", {}).get("content", "")
        }
    else:
        message = {
            "role": "assistant",
            "content": ""
        }

    return {
        "id": openai_data.get("id"),
        "model": openai_data.get("model"),
        "created": openai_data.get("created"),
        "message": message,
        "usage": openai_data.get("usage", {})
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8028)
