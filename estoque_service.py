from app.models.estoque import Estoque
from app.repositories.estoque_repository import EstoqueRepository

class EstoqueService:
    def __init__(self):
        self.repository = EstoqueRepository()

    def create_estoque(self, estoque_schema: EstoqueSchema):
        estoque = Estoque(produto_id=estoque_schema.produto_id, quantidade=estoque_schema.quantidade)
        self.repository.create(estoque)
        return estoque