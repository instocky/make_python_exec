# src/executor.py
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Guards import safer_getattr
from typing import Dict, Any
import requests  # Добавляем импорт
import time     # Добавляем импорт

def _getitem_(obj, key):
    """Безопасный доступ к элементам"""
    return obj[key]

def _getattr_(obj, name):
    """Безопасный доступ к атрибутам"""
    return getattr(obj, name)

SAFE_GLOBALS = {
    'abs': abs,
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'print': print,
    'range': range,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    'round': round,
    'pow': pow,
    'map': map,
    'filter': filter,
    'enumerate': enumerate,
    'zip': zip,
    '__getattr__': safer_getattr,
    '_getitem_': _getitem_,
    '_getiter_': lambda x: iter(x),
    '_iter_unpack_sequence_': lambda x, y: list(x)[:y],
    '_getattr_': _getattr_,  # Добавили guard для атрибутов
    'requests': requests,  # Добавляем requests
    'time': time,         # Добавляем time
}

def execute_code(code: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        globals_dict = SAFE_GLOBALS.copy()
        globals_dict['data'] = input_data
        
        byte_code = compile_restricted(code, '<string>', 'exec')
        locals_dict = {}
        
        exec(byte_code, globals_dict, locals_dict)
        
        return {
            'success': True,
            'result': locals_dict.get('result', None)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }