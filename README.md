# Enterprise AI Chatbot Backend

This is the backend service for an Enterprise Conversational AI Chatbot using Google's Gemini 1.5 Flash model.

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

3. Create a `.env` file:

```bash
cp .env.example .env
```

4. Add your Gemini API key to the `.env` file:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Running the Server

Start the server with:

```bash
uvicorn src.main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Chat Endpoint

- **POST** `/chat`
  - Request body:
    ```json
    {
      "messages": [
        {
          "role": "user",
          "content": "Your message here"
        }
      ],
      "temperature": 0.7,
      "max_tokens": 1000
    }
    ```
  - Response:
    ```json
    {
      "response": "AI response here"
    }
    ```

### Health Check

- **GET** `/health`
  - Returns server status

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
