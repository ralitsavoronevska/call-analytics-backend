from fastapi import FastAPI

from app.api.routes.analytics import router as analytics_router
from app.api.routes.calls import router as calls_router
from app.api.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Call Analytics API",
    description="Secure backend for the Call Analytics Dashboard",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://call-analytics-dashboard-xi.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(calls_router)
app.include_router(analytics_router)
app.include_router(auth_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok"}