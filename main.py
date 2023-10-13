import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configs import get_config
from database import engine
from models import BaseList
from helpers import response_parser
from api.v1 import api

logging.basicConfig(
    filename="weprocess.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

for base in BaseList:
    base.metadata.create_all(engine.db_engine)

env_variables = get_config.get_settings()

app = FastAPI(title=env_variables.app_name, version=env_variables.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return response_parser.generate_response(
        data={"WeProcess": "API Docs"}, message="Working API Setup"
    )


app.include_router(api.router, prefix="/backend/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
