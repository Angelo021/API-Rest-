# Projeto FastAPI com SQLAlchemy

## Configuração

1. Clone o repositório
2. Copie `.env.example` para `.env` e configure as variáveis
3. Execute com Docker:
   ```bash
   docker-compose up --build


5.1.1  
Independência semântica: Produto e Estoque são conceitos distintos - um produto pode existir sem estoque (ex: produto descontinuado), mas estoque não existe sem produto.

Escalabilidade: Permite futuros tipos de estoque (múltiplos armazéns, lote, validade) sem alterar a tabela de produtos.

Integridade referencial: A FK garante que não haja estoque órfão, mantendo consistência.

5.1.2 
Justificativa:
Camada	Regras colocadas	Motivo
Pydantic	Validações sintáticas (tipos, formato, ranges básicos)	Validação precoce, retorno rápido, evita acesso ao banco desnecessário
Service	Regras de negócio (existência, estados, relações)	Acesso a banco de dados, lógica transacional, orquestração

5.1.3 
Mudança no entendimento do domínio:
Antes	Depois
Estoque apenas armazenava quantidade	Estoque tem ciclo de vida (ativo/reservado/baixo/sem_estoque)
Sistema sem controle de concorrência	Sistema com optimistic locking via version
Deletar produto = deletar estoque	Produto pode ser desativado mantendo histórico

5.1.4 
Justificativa:
Por que não Pessimistic Lock?

Menos escalável para leitura frequente

Risco de deadlock em operações rápidas

Comportamento correto:

Ambos usuários carregam estoque (version=1, quantidade=10)

Usuário A dá baixa de 3 → update com WHERE version=1 → sucesso (version=2, quantidade=7)

5.1.5 
Estados terminais: DESCONTINUADO e CANCELADO
Por que não faz sentido retornar de um estado terminal:

Imutabilidade histórica: Produto descontinuado representa uma decisão comercial final. Reativar seria um produto novo (com novo ID), não a mesma entidade.

5.2.1 
Regra: Produto não é deletado fisicamente se tem estoque - apenas marcado como inativo.

5.2.2
def dar_baixa(self, produto_id: int, quantidade: int):
    with self.db.begin():
        estoque = self.estoque_repository.get_by_produto_id_with_lock(produto_id)
        
        if quantidade > estoque.quantidade:
            raise EstoqueInsuficienteException(
                f"Estoque atual: {estoque.quantidade}, solicitado: {quantidade}"
            )
        
        novo_estoque = estoque.quantidade - quantidade
        estoque.quantidade = novo_estoque
        
        # Ações automáticas quando atinge zero
        if novo_estoque == 0:
            estoque.status = EstoqueStatus.SEM_ESTOQUE
            self._notificar_falta_estoque(produto_id)
            self._criar_pedido_reposicao_automatico(produto_id)
        elif novo_estoque < 5:  # Threshold configurável
            estoque.status = EstoqueStatus.BAIXO
            self._notificar_estoque_baixo(produto_id, novo_estoque)
        
        self.estoque_repository.update(estoque)

5.2.3
def adicionar_estoque(self, estoque_id: int, quantidade: int):
    estoque = self.estoque_repository.get_by_id(estoque_id)
    
    if estoque.status in [EstoqueStatus.DESCONTINUADO, EstoqueStatus.CANCELADO]:
        raise EstadoTerminalException(
            f"Estoque está em estado terminal '{estoque.status}'. "
            "Para adicionar estoque, crie um novo registro ou reative o produto."
        )
    
    # Lógica normal de adição...
    estoque.quantidade += quantidade
    if estoque.quantidade > 0 and estoque.status == EstoqueStatus.SEM_ESTOQUE:
        estoque.status = EstoqueStatus.ATIVO

5.2.4
def reservar_estoque(self, produto_id: int, quantidade: int, data_inicio: date, data_fim: date):
    # Verifica sobreposição de reservas
    reservas_conflitantes = self.db.query(ReservaEstoque).filter(
        ReservaEstoque.produto_id == produto_id,
        ReservaEstoque.status == 'ativa',
        ReservaEstoque.data_inicio < data_fim,
        ReservaEstoque.data_fim > data_inicio
    ).all()
    
    if reservas_conflitantes:
        raise DataOverlapException(
            f"Período conflita com reservas: {[(r.data_inicio, r.data_fim) for r in reservas_conflitantes]}"
        )
    
    # Lógica de reserva...

5.2.5 
def transferir_estoque(self, origem_id: int, destino_id: int, quantidade: int):
    """
    Transferência entre armazéns - nunca pode resultar em negativo
    """
    with self.db.begin():
        origem = self.estoque_repository.get_by_id_with_lock(origem_id)
        
        # Validação antes de qualquer modificação
        if origem.quantidade - quantidade < 0:
            raise CalculoNegativoException(
                f"Transferência de {quantidade} resultaria em estoque negativo "
                f"({origem.quantidade} atual no armazém de origem)"
            )
        
        # Aplica em ordem para nunca ter negativo
        origem.quantidade -= quantidade
        destino = self.estoque_repository.get_by_id_with_lock(destino_id)
        destino.quantidade += quantidade
        
        self.estoque_repository.bulk_update([origem, destino])