# src/manage_keys.py
import json
import uuid
from datetime import datetime
from pathlib import Path

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

def add_api_key(name, description, rate_limit, environment='prod'):
    """Добавление нового API ключа"""
    api_keys = load_api_keys()
    
    new_key = generate_api_key(f"sk_{environment}")
    api_keys[new_key] = {
        "name": name,
        "description": description,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "rate_limit": rate_limit
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

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='API Key Management')
    subparsers = parser.add_subparsers(dest='command')
    
    # Команда для добавления ключа
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--name', required=True)
    add_parser.add_argument('--description', required=True)
    add_parser.add_argument('--rate-limit', type=int, default=100)
    add_parser.add_argument('--env', choices=['prod', 'test'], default='prod')
    
    # Команда для просмотра ключей
    subparsers.add_parser('list')
    
    # Команда для отзыва ключа
    revoke_parser = subparsers.add_parser('revoke')
    revoke_parser.add_argument('key')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        key = add_api_key(args.name, args.description, args.rate_limit, args.env)
        print(f"Added new API key: {key}")
    elif args.command == 'list':
        list_api_keys()
    elif args.command == 'revoke':
        if revoke_api_key(args.key):
            print(f"Revoked API key: {args.key}")
        else:
            print("Key not found")