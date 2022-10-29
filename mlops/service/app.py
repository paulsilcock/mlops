from typing import TypedDict
from fastapi import FastAPI
from mlops.service.predictor import ResponsePredictor

app = FastAPI()

predictor = ResponsePredictor("path_to_model_file")


class NewMessagePayload(TypedDict):
    message: str


@app.post("/messages/new")
async def send_message(request_body: NewMessagePayload):
    return predictor.predict(request_body["message"])
