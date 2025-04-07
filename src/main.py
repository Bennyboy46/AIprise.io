from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Enterprise AI Chatbot")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Enterprise-specific system prompt
ENTERPRISE_PROMPT = """You are an Enterprise AI Assistant specialized in business and professional services. 
Your expertise includes:
- Business strategy and operations
- Enterprise software and technology
- Corporate communications
- Project management
- Data analysis and business intelligence
- Professional services and consulting
- Industry-specific knowledge (finance, healthcare, manufacturing, etc.)

Always maintain a professional tone and focus on:
- Clear, concise business communication
- Data-driven insights
- Industry best practices
- Enterprise security and compliance
- Scalable solutions
- ROI and business value

Format responses in a professional manner with:
- Clear structure and headings
- Bullet points for key points
- Data and metrics when relevant
- Actionable recommendations
- Professional terminology

Remember to:
- Maintain confidentiality
- Consider enterprise security
- Focus on business value
- Use industry-standard practices
- Provide evidence-based insights
"""

@app.post("/chat")
async def chat(request: Dict[str, Any]):
    try:
        # Validate request structure
        if "messages" not in request or not isinstance(request["messages"], list):
            raise HTTPException(status_code=400, detail="Invalid request format: messages field is required")
        
        messages = request["messages"]
        if not messages:
            raise HTTPException(status_code=400, detail="Messages list cannot be empty")
        
        # Get the last user message
        last_message = messages[-1]
        if not isinstance(last_message, dict) or "role" not in last_message or "content" not in last_message:
            raise HTTPException(status_code=400, detail="Invalid message format")
        
        if last_message["role"] != "user":
            raise HTTPException(status_code=400, detail="Last message must be from user")
        
        # Add enterprise context to the message
        enterprise_message = f"{ENTERPRISE_PROMPT}\n\nUser Query: {last_message['content']}"
        
        # Generate response
        chat = model.start_chat(history=[])
        response = chat.send_message(enterprise_message)
        
        return {"response": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 