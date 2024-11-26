# Python Code Executor API

Simple REST API service that executes Python code in a restricted environment. Version 0.1.1126

## Features

- Execute Python code via REST API
- Restricted execution environment for safety
- Support for basic Python operations and built-in functions
- JSON input/output

## Installation

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
python-executor/
    ├── src/
    │   ├── __init__.py
    │   ├── main.py       # FastAPI application
    │   └── executor.py   # Code execution engine
    └── requirements.txt
```

## Usage

### Start the Server

```bash
uvicorn src.main:app --reload
```

Server will start at http://localhost:8000

### API Endpoints

#### POST /execute

Execute Python code with provided data.

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

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- RestrictedPython
- Pydantic

## Version

0.1.1126 - Initial prototype
- Basic code execution
- Restricted environment
- JSON API

## License

MIT

