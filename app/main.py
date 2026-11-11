"""FastAPI entry point for the Customer Support Resolution Agent."""

from fastapi import FastAPI

app = FastAPI(
    title="Customer Support Resolution Agent",
    description="Human-in-the-loop support resolution workflow.",
    version="0.1.0",
)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    """Basic liveness check."""
    return {"status": "ok"}
