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


Identificador	RN-001
Nome	Integridade de estoque não negativo
Gatilho	Ao dar baixa, reservar ou atualizar estoque (métodos que diminuem quantidade)
Pré-condição	Estoque existe e está em estado não terminal (ATIVO, BAIXO, SEM_ESTOQUE ou RESERVADO)
Ação	Sistema calcula nova_quantidade = quantidade_atual - quantidade_solicitada. Se nova_quantidade < 0, rejeita a operação e retorna erro. Se válida, executa a atualização e registra movimentação.
Violação	HTTP Status: 400 Bad Request
Payload:

Identificador	RN-002
Nome	Controle de concorrência via optimistic locking
Gatilho	Ao atualizar qualquer atributo do estoque (quantidade ou status)
Pré-condição	Cliente fornece a versão atual do registro (obtida na última leitura)
Ação	Sistema verifica se version recebida == version atual no banco. Se igual, atualiza e incrementa version. Se diferente, rejeita com erro de concorrência. Implementa retry com backoff exponencial (3 tentativas).
Violação	HTTP Status: 409 Conflict
Payload:

Identificador	RN-003
Nome	Imutabilidade de estados terminais
Gatilho	Ao tentar modificar um estoque em estado DESCONTINUADO ou CANCELADO (qualquer operação que não seja leitura)
Pré-condição	Estoque existe e está em estado terminal (DESCONTINUADO ou CANCELADO)
Ação	Sistema rejeita qualquer operação de modificação (atualização, baixa, reserva). Apenas consultas são permitidas. Para modificar, é necessário criar um novo registro de estoque.
Violação	HTTP Sta

Identificador	RN-004
Nome	Proteção de exclusão de produto com estoque
Gatilho	Ao tentar deletar (DELETE) um produto que possui estoque
Pré-condição	Produto existe e não foi previamente deletado (soft delete)
Ação	Sistema verifica se o estoque associado tem quantidade > 0. Se positivo, rejeita a exclusão e orienta o usuário a zerar o estoque primeiro. O produto só pode ser deletado via soft delete quando estoque = 0.
Violação	HTTP Status: 409 Conflict
Payload:

Identificador	RN-005
Nome	Alerta de estoque baixo
Gatilho	Ao atualizar quantidade de estoque (entrada, saída, ajuste)
Pré-condição	Estoque existe e a nova quantidade é ≥ 0
Ação	Após cada atualização, sistema verifica: se nova_quantidade < ESTOQUE_BAIXO_THRESHOLD (default=5) e nova_quantidade > 0, muda status para BAIXO e dispara notificação (email/slack/log). Se nova_quantidade == 0, muda para SEM_ESTOQUE. Se nova_quantidade >= 5 e estava em BAIXO, muda para ATIVO.
Violação	Esta regra não gera erro, mas sim um evento de notificação. Se o sistema de notificação falhar, registra erro em log mas não interrompe a operação principal.
Justificativa	Previne ruptura de estoque. Time de compras precisa ser alertado antes que o produto acabe completamente.


