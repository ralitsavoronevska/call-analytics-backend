from fastapi import FastAPI

from app.api.routes.analytics import router as analytics_router
from app.api.routes.calls import router as calls_router


app = FastAPI(
    title="Call Analytics API",
    description="Secure backend for the Call Analytics Dashboard",
    version="1.0.0",
)

app.include_router(calls_router)
app.include_router(analytics_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok"}