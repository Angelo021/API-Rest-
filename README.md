# Sistema de Gerenciamento de Produtos e Estoque

## Descrição do Domínio

O sistema gerencia o ciclo de vida de produtos e seus respectivos estoques em uma operação comercial. O domínio abrange:

- **Produtos**: Itens comercializáveis com nome e descrição
- **Estoque**: Quantidade disponível de cada produto com controle de estado
- **Movimentações**: Operações de entrada, saída e reserva de estoque
- **Transições de estado**: Ciclo de vida do estoque (ativo → reservado → baixo → sem_estoque → descontinuado/cancelado)

### Conceitos principais:
- Um **Produto** pode existir sem Estoque (ex: produto planejado, não lançado)
- Um **Estoque** sempre pertence a um único Produto (relacionamento 1:1)
- **Estados terminais** (descontinuado, cancelado) são irreversíveis por razões de auditoria
- **Versionamento** otimista previne race conditions em movimentações concorrentes

## Diagrama ER

<img width="918" height="852" alt="Captura de tela_15-6-2026_134053_www make-charts com" src="https://github.com/user-attachments/assets/6b67ce1e-e4cb-4aec-bc09-f4c84a062d70" />

## Como Rodar Localmente

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+ (para execução sem Docker)
- PostgreSQL 15+
## Execute com Docker Compose
docker-compose up --build



