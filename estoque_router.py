from fastapi import APIRouter
from app.services.estoque_service import EstoqueService
from app.schemas.estoque import EstoqueSchema

router = APIRouter()

@router.post("/estoques")
async def create_estoque(estoque_schema: EstoqueSchema):
    service = EstoqueService()
    estoque = service.create_estoque(estoque_schema)
    return {"id": estoque.id, "produto_id": estoque.produto_id, "quantidade": estoque.quantidade}