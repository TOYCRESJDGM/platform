import uvicorn
from fastapi import FastAPI
from src.routes import invoice
from dotenv import load_dotenv
from src.utils.logger import logger
from contextlib import asynccontextmanager
from src.adapters.mysql_adapter import create_db
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from src.utils.settings import APP_PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start Service...")
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Hello from docker"}


# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(
    invoice.router,
    prefix="/api/v1",
    tags=["invoice"],
    responses={404: {"description": "Not found"}},
)


if __name__ == "__main__":
    logger.info("Start service on port {APP_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=[APP_PORT, 5000])