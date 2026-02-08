from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

summarizer = None




class summarizeRequest(BaseModel):
    text: str


@app.get("/")
def health_check():
    return{
        "status": "running",
        "message": "AI Text APi alive"
    }

def load_model():
    global summarizer
    if summarizer is None:
        summarizer = pipeline(
            "summarization",
            model="sshleifer/tiny-t5"
        )

@app.post('/summarize')
def summarize_text(request: summarizeRequest):


    try:
        if not request.text.strip():
             return{
                  "Error":"Text cannot be empty"
             }
        
        load_model()

        summary = summarizer(
             request.text,
               max_length=60,
                min_length=20,
                do_sample=False
        )

        return{
             "summary":summary[0]["summary_text"]
        }
    
    except Exception as e:
        return{
            "error" : str(e),
             "type":type(e).__name___
        }