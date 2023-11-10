
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.s3 import s3_controller
from app.controllers.rds import rds_controller

app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # Allows all origins
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/endpoint_post")
async def endpoint_post(body: dict, path:str)-> str:
    return s3_controller.insert_json(body, path)

@app.get("/endpoint_get")
async def endpoint_get(table_name:str)-> dict:
    data = rds_controller.get_information(table_name)
    return data

