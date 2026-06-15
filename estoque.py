from pydantic import BaseModel

class EstoqueSchema(BaseModel):
    produto_id: int
    quantidade: int