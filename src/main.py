# src/main.py
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Dict, Any
import os
from dotenv import load_dotenv
from pathlib import Path
from .executor import execute_code

# Загружаем переменные окружения из .env файла
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Получаем API ключ из переменных окружения
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable is not set")

app = FastAPI(title="Python Code Executor API")

# Создаем схему безопасности для API ключа
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Проверка API ключа"""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return api_key

class CodeExecutionRequest(BaseModel):
    code: str
    data: Dict[str, Any]

@app.post("/execute")
async def execute(
    request: CodeExecutionRequest,
    api_key: str = Depends(verify_api_key)
):
    result = execute_code(request.code, request.data)
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
        
    return result