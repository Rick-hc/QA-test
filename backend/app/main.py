import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="QA Search API")

if os.getenv("ENV", "dev") == "dev":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

from .routers import query, search, answer, feedback

app.include_router(query.router)
app.include_router(search.router)
app.include_router(answer.router)
app.include_router(feedback.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
