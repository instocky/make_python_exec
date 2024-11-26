# src/main.py
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Dict, Any
import json
from pathlib import Path
from .executor import execute_code

API_KEYS_FILE = Path(__file__).parent / 'api_keys.json'

def load_api_keys():
    if not API_KEYS_FILE.exists():
        with open(API_KEYS_FILE, 'w') as f:
            json.dump({}, f, indent=4)
        return {}
    
    with open(API_KEYS_FILE) as f:
        return json.load(f)

def save_api_keys(api_keys):
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, indent=4, fp=f)

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
    
    client_info = API_KEYS[api_key]
    if client_info['executions_left'] <= 0:
        raise HTTPException(
            status_code=403,
            detail="API executions limit exceeded"
        )
    
    return {
        'key': api_key,
        'client_info': client_info
    }

class CodeExecutionRequest(BaseModel):
    code: str
    data: Dict[str, Any]

@app.post("/execute")
async def execute(
    request: CodeExecutionRequest,
    auth_info: dict = Depends(verify_api_key)
):
    key = auth_info['key']
    client_info = auth_info['client_info']
    
    # Выполняем код
    result = execute_code(request.code, request.data)
    
    if result['success']:
        # Уменьшаем счетчик оставшихся выполнений
        API_KEYS[key]['executions_left'] -= 1
        save_api_keys(API_KEYS)
        
        # Добавляем информацию об оставшихся выполнениях в ответ
        result['executions_left'] = API_KEYS[key]['executions_left']
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
        
    return result