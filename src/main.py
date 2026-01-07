from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api.routes import router as api_router

app = FastAPI(title="Zelyo Config Guardian")

app.include_router(api_router)

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/redoc")
