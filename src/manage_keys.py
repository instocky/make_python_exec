# src/manage_keys.py
import json
import uuid
from datetime import datetime
from pathlib import Path
import argparse

API_KEYS_FILE = Path(__file__).parent / 'api_keys.json'

def load_api_keys():
    """Загрузка существующих API ключей"""
    if not API_KEYS_FILE.exists():
        return {}
    
    with open(API_KEYS_FILE) as f:
        return json.load(f)

def save_api_keys(api_keys):
    """Сохранение API ключей в файл"""
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, indent=4, fp=f)

def generate_api_key(prefix='sk'):
    """Генерация нового API ключа"""
    unique_id = uuid.uuid4().hex[:12]
    return f"{prefix}_{unique_id}"

def add_api_key(name, description, rate_limit, executions_limit, environment='prod'):
    """Добавление нового API ключа"""
    api_keys = load_api_keys()
    
    new_key = generate_api_key(f"sk_{environment}")
    api_keys[new_key] = {
        "name": name,
        "description": description,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "rate_limit": rate_limit,
        "executions_limit": executions_limit,
        "executions_left": executions_limit
    }
    
    save_api_keys(api_keys)
    return new_key

def list_api_keys():
    """Вывод списка всех API ключей"""
    api_keys = load_api_keys()
    if not api_keys:
        print("No API keys found")
        return
        
    for key, info in api_keys.items():
        print(f"\nKey: {key}")
        for field, value in info.items():
            print(f"  {field}: {value}")

def revoke_api_key(key):
    """Отзыв API ключа"""
    api_keys = load_api_keys()
    if key in api_keys:
        del api_keys[key]
        save_api_keys(api_keys)
        return True
    return False

def reset_executions(key):
    """Сброс счетчика выполнений"""
    api_keys = load_api_keys()
    if key in api_keys:
        api_keys[key]['executions_left'] = api_keys[key]['executions_limit']
        save_api_keys(api_keys)
        return True
    return False

def update_executions_limit(key, new_limit):
    """Обновление лимита выполнений"""
    api_keys = load_api_keys()
    if key in api_keys:
        api_keys[key]['executions_limit'] = new_limit
        api_keys[key]['executions_left'] = new_limit
        save_api_keys(api_keys)
        return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='API Key Management')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Команда для добавления ключа
    add_parser = subparsers.add_parser('add', help='Add new API key')
    add_parser.add_argument('--name', required=True, help='Client name')
    add_parser.add_argument('--description', required=True, help='Client description')
    add_parser.add_argument('--rate-limit', type=int, default=100, help='Rate limit per minute')
    add_parser.add_argument('--executions-limit', type=int, default=1000, help='Total executions limit')
    add_parser.add_argument('--env', choices=['prod', 'test'], default='prod', help='Environment (prod/test)')
    
    # Команда для просмотра ключей
    subparsers.add_parser('list', help='List all API keys')
    
    # Команда для отзыва ключа
    revoke_parser = subparsers.add_parser('revoke', help='Revoke API key')
    revoke_parser.add_argument('key', help='API key to revoke')
    
    # Команда для сброса счетчика
    reset_parser = subparsers.add_parser('reset-executions', help='Reset executions counter')
    reset_parser.add_argument('key', help='API key to reset')
    
    # Команда для обновления лимита выполнений
    update_parser = subparsers.add_parser('update-limit', help='Update executions limit')
    update_parser.add_argument('key', help='API key to update')
    update_parser.add_argument('new_limit', type=int, help='New executions limit')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        key = add_api_key(args.name, args.description, args.rate_limit, 
                         args.executions_limit, args.env)
        print(f"Added new API key: {key}")
        
    elif args.command == 'list':
        list_api_keys()
        
    elif args.command == 'revoke':
        if revoke_api_key(args.key):
            print(f"Revoked API key: {args.key}")
        else:
            print("Key not found")
            
    elif args.command == 'reset-executions':
        if reset_executions(args.key):
            print(f"Reset executions counter for key: {args.key}")
        else:
            print("Key not found")
            
    elif args.command == 'update-limit':
        if update_executions_limit(args.key, args.new_limit):
            print(f"Updated executions limit for key: {args.key} to {args.new_limit}")
        else:
            print("Key not found")
            
    elif not args.command:
        parser.print_help()