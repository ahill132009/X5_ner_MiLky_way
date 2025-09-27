from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model_processing.loader import Model 
from config import settings
from api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Loading NER model...")
    model = Model(settings.model_dir, settings.tokenizer_dir)
    app.state.loaded_model = model.init_model()
    print("✅ NER model loaded.")
    yield
    # Shutdown
    print("🧹 Unloading NER model...")
    app.state.loaded_model = None
    print("👋 NER model unloaded.")

app = FastAPI(
    title="X5 NER",
    description="Сервис для хакатона X5",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/", include_in_schema=False)
async def root():
    return JSONResponse({"status": "ok", "service": "X5 NER"})