from fastapi import FastAPI

app = FastAPI(
    title="Call Analytics API",
    description="Secure backend for the Call Analytics Dashboard",
    version="1.0.0",
)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok"}