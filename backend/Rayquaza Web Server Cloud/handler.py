from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="Rayquaza Cloud Web Server")

@app.get("/")
def index():
    return {
        "status": "ONLINE",
        "service": "Rayquaza Web Server Cloud",
        "environment": "AWS Lambda Serverless"
    }

# Lambda Handler integration
handler = Mangum(app)
