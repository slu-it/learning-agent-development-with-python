"""FastAPI server exposing the message delivery agent over HTTP.

Start it with:
    uv run uvicorn app.server:app --reload

Then POST a query:
    curl -X POST http://localhost:8000/query \\
        -H "Content-Type: application/json" \\
        -d '{"query": "Send a WhatsApp to Alice Johnson saying hi"}'
"""

import logging

from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import run_agent

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Message Delivery Agent")


class QueryRequest(BaseModel):
    query: str


class QueryReply(BaseModel):
    reply: str


@app.post("/query", response_model=QueryReply)
async def query(request: QueryRequest) -> QueryReply:
    """Feed the query into the agent loop and return its final reply."""
    reply = await run_agent(request.query)
    return QueryReply(reply=reply)


@app.get("/health")
def health() -> dict[str, str]:
    """Simple liveness check."""
    return {"status": "ok"}
