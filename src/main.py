from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api.routes import router as api_router

app = FastAPI(
    title="Zelyo Config Guardian",
    description="Kubernetes configuration guardian with LLM-powered remediation and MCP integration.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(api_router)

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")
