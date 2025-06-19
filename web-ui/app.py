from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx
import json
import os
import logging
from typing import Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Настройка шаблонов и статических файлов
templates = Jinja2Templates(directory="templates")
# Раскомментировать если будет папка static
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Конфигурация из переменных окружения
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'deepseek-r1')
WEB_UI_PORT = os.getenv('WEB_UI_PORT', 8080)
OLLAMA_HOST = os.getenv('OLLAMA_HOST', '0.0.0.0')

# Pydantic модели для валидации данных
class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = OLLAMA_MODEL


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/models")
async def get_models():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{OLLAMA_BASE_URL}/api/tags')
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=500, detail='Failed to fetch models')
    except httpx.RequestError as e:
        logger.error(f"Request error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(chat_request: ChatRequest):
    try:
        if not chat_request.message:
            raise HTTPException(status_code=400, detail='Message is required')

        # Отправляем запрос к Ollama
        ollama_data = {
            'model': chat_request.model,
            'prompt': chat_request.message,
            'stream': False
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f'{OLLAMA_BASE_URL}/api/generate',
                json=ollama_data
            )

            if response.status_code == 200:
                result = response.json()
                return {'response': result.get('response', 'No response')}
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f'Ollama API error: {response.status_code}'
                )

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail='Request timeout')
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream")
async def chat_stream(chat_request: ChatRequest):
    try:
        if not chat_request.message:
            raise HTTPException(status_code=400, detail='Message is required')

        async def generate():
            ollama_data = {
                'model': chat_request.model,
                'prompt': chat_request.message,
                'stream': True
            }

            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    async with client.stream(
                        'POST',
                        f'{OLLAMA_BASE_URL}/api/generate',
                        json=ollama_data
                    ) as response:
                        async for line in response.aiter_lines():
                            if line:
                                try:
                                    chunk = json.loads(line)
                                    if 'response' in chunk:
                                        yield f"data: {json.dumps({'response': chunk['response']})}\n\n"
                                    if chunk.get('done', False):
                                        yield f"data: {json.dumps({'done': True})}\n\n"
                                        break
                                except json.JSONDecodeError:
                                    continue

            except Exception as e:
                logger.error(f"Stream error: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(generate(), media_type='text/plain')

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat stream error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=OLLAMA_HOST, port=WEB_UI_PORT)