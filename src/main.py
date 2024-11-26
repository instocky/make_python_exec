# src/main.py
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Dict, Any
import json
from pathlib import Path
from .executor import execute_code

# Путь к файлу с API ключами
API_KEYS_FILE = Path(__file__).parent / 'api_keys.json'

# Загрузка API ключей
def load_api_keys():
    if not API_KEYS_FILE.exists():
        with open(API_KEYS_FILE, 'w') as f:
            json.dump({}, f, indent=4)
        return {}
    
    with open(API_KEYS_FILE) as f:
        return json.load(f)

API_KEYS = load_api_keys()

app = FastAPI(title="Python Code Executor API")

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Проверка API ключа и получение информации о клиенте"""
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return {
        'key': api_key,
        'client_info': API_KEYS[api_key]
    }

class CodeExecutionRequest(BaseModel):
    code: str
    data: Dict[str, Any]

@app.post("/execute")
async def execute(
    request: CodeExecutionRequest,
    auth_info: dict = Depends(verify_api_key)
):
    client_name = auth_info['client_info'].get('name', 'Unknown Client')
    print(f"Executing code for client: {client_name}")
    
    result = execute_code(request.code, request.data)
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
        
    return result