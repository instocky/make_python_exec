# Python Code Executor API

Simple REST API service that executes Python code in a restricted environment. Version 0.1.1126

## Features

- Execute Python code via REST API
- Restricted execution environment for safety
- Support for basic Python operations and built-in functions
- JSON input/output
- API key authentication with client management
- Support for multiple clients with different environments (test/prod)

## Installation

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp src/api_keys.json.sample src/api_keys.json
python src/manage_keys.py add --name "Test Client" --description "For testing" --env test
```

## Project Structure

```
python-executor/
    ├── src/
    │   ├── __init__.py
    │   ├── main.py          # FastAPI application
    │   ├── executor.py      # Code execution engine
    │   ├── manage_keys.py   # API key management tool
    │   ├── api_keys.json    # API keys storage (not in git)
    │   └── api_keys.json.sample  # Example API keys structure
    ├── requirements.txt
    └── .gitignore
```

## API Key Management

The service uses API key authentication. Keys can be managed using the CLI tool:

```bash
# Add a new key
python src/manage_keys.py add --name "Client Name" --description "Description" --env prod

# List all keys
python src/manage_keys.py list

# Revoke a key
python src/manage_keys.py revoke sk_prod_xyz789
```

Note: The `api_keys.json` file contains sensitive information and should never be committed to the repository.

## Usage

### Start the Server

```bash
uvicorn src.main:app --reload
```

Server will start at http://localhost:8000

### API Endpoints

#### POST /execute

Execute Python code with provided data. Requires API key authentication.

**Headers:**
```
X-API-Key: your_api_key
Content-Type: application/json
```

**Request Body:**
```json
{
    "code": "result = sum(data['numbers']) / len(data['numbers'])",
    "data": {
        "numbers": [1, 2, 3, 4, 5]
    }
}
```

**Response:**
```json
{
    "success": true,
    "result": 3.0
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/execute \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"code": "result = data[\"x\"] + data[\"y\"]", "data": {"x": 1, "y": 2}}'
```

### Available Functions

The following Python built-in functions are available in the restricted environment:
- abs, bool, dict, float, int
- len, list, max, min, print
- range, str, sum, tuple
- round, pow
- map, filter, enumerate, zip

### Safety Features

- Restricted execution environment using RestrictedPython
- No file system access
- No network access
- No module imports
- Limited to basic Python operations
- API key authentication
- Client-specific rate limits and monitoring

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- RestrictedPython
- Pydantic

## Version History

0.1.1126
- Initial prototype with basic code execution
- Restricted environment
- JSON API
- API key authentication system
- Multiple client support with metadata

## License

MIT