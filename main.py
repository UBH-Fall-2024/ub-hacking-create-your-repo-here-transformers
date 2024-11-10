import prompt
import persist
from fastapi import FastAPI

app = FastAPI()

@app.get("/ask")
async def ask_question():
    question = '''
        After reviewing the context, generate 3 follow-up questions. Provide your responses in the following numeric format for easy processing by the front end:
        1. [First follow-up question]
        2. [Second follow-up question]
        3. [Third follow-up question]
    '''
    
    persist.persist_data(question)
    
    result = prompt.prompt(question=question)
    
    return result
