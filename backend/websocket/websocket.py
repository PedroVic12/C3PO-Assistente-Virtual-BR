from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)
