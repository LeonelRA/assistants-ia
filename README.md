# OpenAI FastAPI Integration

This is a simple FastAPI application that integrates with OpenAI's API to provide chat functionality.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

Start the server:

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## API Endpoints

- `GET /`: Welcome message
- `POST /chat`: Send a message to OpenAI's GPT-3.5-turbo model

Example chat request:

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, how are you?"}'
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

/app
├── main.py # Punto de entrada de la app (instancia de FastAPI)
├── api/ # Define rutas (routers)
│ ├── **init**.py
│ ├── users.py # Rutas relacionadas al recurso "users"
│ └── items.py # Otro recurso
├── models/ # Modelos SQLAlchemy
│ ├── **init**.py
│ └── user.py
├── schemas/ # Pydantic schemas (request/response)
│ ├── **init**.py
│ └── user.py
├── crud/ # Operaciones CRUD con la DB
│ ├── **init**.py
│ └── user.py
├── db/ # Configuración de la base de datos
│ ├── **init**.py
│ ├── base.py # Base de modelos
│ └── session.py # Session y engine
└── core/ # Configuración del proyecto
├── **init**.py
└── config.py # Variables de entorno, settings
