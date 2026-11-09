import os

os.environ["HF_HOME"] = "C:/huggingface_cache"
os.environ["TRANSFORMERS_CACHE"] = "C:/huggingface_cache"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = FastAPI(title="Tradutor EN-DE com LangChain & HuggingFace")

MODEL_NAME = "Helsinki-NLP/opus-mt-en-de"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto em inglês")

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str

@app.post("/translate", response_model=TranslationResponse)
async def translate(data: TranslationRequest):
    try:
        inputs = tokenizer(data.text, return_tensors="pt", padding=True)
        translated_tokens = model.generate(**inputs)
        result = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

        return {
            "original_text": data.text,
            "translated_text": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))