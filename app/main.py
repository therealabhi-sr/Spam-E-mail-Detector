from fastapi import FastAPI

from schemas import EmailRequest
from inference import predict_email

app=FastAPI()

@app.get("/")
def home():
    return {"message":"spam detaction api running"}


@app.post("/predict")
def predict(data:EmailRequest):
    result=predict_email(data.email)

    return result