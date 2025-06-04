import os
import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from src.utils import aggregate_ner_results

app = FastAPI()

NER_SERVICE_URL = os.getenv('NER_SERVICE_URL', 'http://localhost:3000')

@app.get("/")
async def serve_gui():
    return FileResponse("static/ner_gui.html")

@app.post("/ner")
async def classify(request: Request):
    # Retrieve the raw string from the request body
    data = await request.json()
    print(f"Received data: {data}")
    text = data.get("text", "")
    
    # We need to make request to the NER service
    ner_response = requests.post(f'{NER_SERVICE_URL}/ner', data=text)
    ner_results = ner_response.json()
    aggregated_results = aggregate_ner_results(ner_results, original_text=text)

    return aggregated_results

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)