from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import query, search, answer, feedback

app = FastAPI(title="QA Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)
app.include_router(search.router)
app.include_router(answer.router)
app.include_router(feedback.router)
