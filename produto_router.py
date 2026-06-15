from fastapi import APIRouter
from app.services.produto_service import ProdutoService
from app.schemas.produto import ProdutoSchema

router = APIRouter()

@router.post("/produtos")
async def create_produto(produto_schema: ProdutoSchema):
    service = ProdutoService()
    produto = service.create_produto(produto_schema)
    return {"id": produto.id, "nome": produto.nome, "descricao": produto.descricao}