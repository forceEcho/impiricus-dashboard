import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
import logging
import time

from app.api.main import api_router
from app.core.config import settings
from app.core.db import init_db
import app.models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

@app.on_event("startup")  
def on_startup():  
    init_db()

@app.middleware("http")  
async def log_request_latency(request: Request, call_next):  
    start_time = time.perf_counter()  
    response = await call_next(request)  
    latency = time.perf_counter() - start_time  
    logging.info(f"Path: {request.url.path} | Method: {request.method} | Latency: {latency:.4f}s")  
    return response  

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.all_cors_origins,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)
