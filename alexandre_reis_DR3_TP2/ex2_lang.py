import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="Tradutor OpenAI com LangChain")

# Certifique-se de configurar a variável OPENAI_API_KEY no ambiente
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um tradutor especialista. Traduza o texto em inglês a seguir para o francês de forma precisa."),
    ("user", "{text}")
])

chain = prompt | llm

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1)

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str

@app.post("/translate", response_model=TranslationResponse)
async def translate(data: TranslationRequest):
    try:
        response = chain.invoke({"text": data.text})
        return {
            "original_text": data.text,
            "translated_text": response.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))