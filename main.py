import prompt
import persist
from fastapi import FastAPI

app = FastAPI()

@app.get("/ask")
async def ask_question():
    question = "How do you setup a For Loop in Python?"
    
    persist.persist_data(question)
    
    result = prompt.prompt(question=question)
    
    return result
