from pydantic import BaseModel

class ProdutoSchema(BaseModel):
    nome: str
    descricao: str