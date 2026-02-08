from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

summarizer = pipeline(
     "summarization",
     model = "sshleifer/distilbart-cnn-12-6"
)


class summarizeRequest(BaseModel):
    text: str


@app.get("/")
def health_check():
    return{
        "status": "running",
        "message": "AI Text APi alive"
    }

@app.post('/summarize')
def summarize_text(request: summarizeRequest):
        if not request.text.strip():
             return{
                  "Error":"Text cannot be empty"
             }
        summary = summarizer(
             request.text,
             max_length = 120,
             min_length = 30,
             do_sample = False
        )

        return{
             "summary":summary[0]["summary_text"]
        }