##  Pré-requisitos

- **Python 3.10+** instalado.
- Chave de API da OpenAI (apenas para a **Parte 2 - Questão 2**).

---

##  Passo a Passo para Instalação e Execução

### 1. Clonar o Repositório e Criar o Ambiente Virtual

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
.\venv\Scripts\Activate.ps1
```

### 2. Instalar as Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

##  Como Executar cada Aplicação

Para rodar cada aplicação, navegue até a pasta correspondente ou execute o `uvicorn` indicando o caminho do arquivo.

###  Parte 1: FastAPI & HuggingFace

#### Questão 1: Gerador de Texto com GPT-2
```bash
uvicorn ex1_api:app --reload
```
- **Endpoint:** `POST http://127.0.0.1:8000/translate`
- **Exemplo de Body JSON:**
```json
{
  "text": "Hello, how are you feeling today?"
}
```

---

###  Parte 2: LangChain

#### Questão 1: Chatbot com Fake LLM
```bash
uvicorn ex1_lang:app --reload
```
- **Endpoint:** `POST http://127.0.0.1:8000/chat`
- **Exemplo de Body JSON:**
```json
{
  "message": "Qual é o status da aplicação?"
}
```

#### Questão 2: Tradutor EN -> FR com OpenAI
>  **Atenção:** Defina sua variável de ambiente `OPENAI_API_KEY` antes de rodar.

```bash

$env:OPENAI_API_KEY="sk-sua-chave-aqui"

# Executar a aplicação
uvicorn ex2_lang:app --reload
```
- **Endpoint:** `POST http://127.0.0.1:8000/translate`
- **Exemplo de Body JSON:**
```json
{
  "text": "Data Science is an essential domain for modern businesses."
}
```

#### Questão 3: Tradutor EN -> DE com HuggingFace & LangChain
```bash
uvicorn ex3_lang:app --reload
```
- **Endpoint:** `POST http://127.0.0.1:8000/translate`
- **Exemplo de Body JSON:**
```json
{
  "text": "Machine learning enables computers to learn from data."
}
```

---

##  Testando as APIs

Todas as aplicações contam com a documentação interativa automática do FastAPI. Com o servidor rodando, acesse em seu navegador:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`