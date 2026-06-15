from fastapi import FastAPI
from app.routers import produto_router, estoque_router

app = FastAPI()

app.include_router(produto_router)
app.include_router(estoque_router)
