from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline, set_seed

app = FastAPI(title="Gerador de Texto com GPT-2")

# Inicialização do pipeline (executado uma vez no carregamento)
generator = pipeline('text-generation', model='gpt2')

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Texto inicial para geração")
    max_length: int = Field(50, ge=10, le=200, description="Tamanho máximo do texto")

class TextResponse(BaseModel):
    prompt: str
    generated_text: str

@app.post("/generate", response_model=TextResponse)
async def generate_text(data: PromptRequest):
    try:
        set_seed(42)
        result = generator(
            data.prompt,
            max_length=data.max_length,
            num_return_sequences=1,
            truncation=True
        )
        return {
            "prompt": data.prompt,
            "generated_text": result[0]['generated_text']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))