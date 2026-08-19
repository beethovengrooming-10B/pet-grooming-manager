from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.animals import router as animals_router
from app.api.clients import router as clients_router

app = FastAPI(
    title="Pet Grooming Manager API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)

app.include_router(clients_router)
app.include_router(animals_router)

@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
