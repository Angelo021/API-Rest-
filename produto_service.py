from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository

class ProdutoService:
    def __init__(self):
        self.repository = ProdutoRepository()

    def create_produto(self, produto_schema: ProdutoSchema):
        produto = Produto(nome=produto_schema.nome, descricao=produto_schema.descricao)
        self.repository.create(produto)
        return produto