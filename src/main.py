from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from .executor import execute_code

app = FastAPI(title="Python Code Executor API")

class CodeExecutionRequest(BaseModel):
    code: str
    data: Dict[str, Any]

@app.post("/execute")
async def execute(request: CodeExecutionRequest):
    result = execute_code(request.code, request.data)
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
        
    return result