import os
os.environ["HF_HOME"] = "C:/huggingface_cache"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

app = FastAPI(title="Tradutor EN-FR")

MODEL_NAME = "Helsinki-NLP/opus-mt-en-fr"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

translator = pipeline(
    task="text-generation", 
    model=model, 
    tokenizer=tokenizer
)

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto em inglês")

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(data: TranslationRequest):
    try:
        result = translator(data.text)
        return {
            "original_text": data.text,
            "translated_text": result[0]['generated_text']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))