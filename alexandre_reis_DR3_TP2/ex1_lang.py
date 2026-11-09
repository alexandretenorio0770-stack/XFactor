# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.llms import FakeListLLM

app = FastAPI(title="Fake LLM Chatbot")

# Simulação de respostas pré-definidas
responses = [
    "Olá! Como posso ajudar você hoje?",
    "Sou um chatbot de teste rodando com Fake LLM.",
    "Tudo funcionando perfeitamente por aqui!"
]
fake_llm = FakeListLLM(responses=responses)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    user_message: str
    bot_response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(data: ChatRequest):
    # Executa a chamada no LLM simulado
    response = fake_llm.invoke(data.message)
    return {
        "user_message": data.message,
        "bot_response": response
    }