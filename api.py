from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="Gemini LangChain API",
    description="Simple API using LangChain and Gemini 3.1 Flash-Lite",
    version="1.0.0"
)

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.7,
    max_tokens=1024
)

# Request schema
class ChatRequest(BaseModel):
    prompt: str

# Response schema
class ChatResponse(BaseModel):
    response: str


@app.get("/")
def home():
    return {"message": "Gemini LangChain API is running!"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = llm.invoke(request.prompt)

    return ChatResponse(
        response=response.content
    )
