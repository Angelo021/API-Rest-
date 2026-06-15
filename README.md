# API-Rest-
# Sistema de Gerenciamento de Produtos e Estoque 

O sistema gerencia o ciclo de vida de produtos e seus respectivos estoques em uma operação comercial. 

- **Produtos** - Itens comercializaveis com nome e descrição
- **Estoque** - Quantidade disponível de cada produto com controle de estado
- **Movimentação** - Operação de entrada , saída e reserva
- **Transições de estado** - Ciclo de vida do estoque ( ativo -> reservado -> baixo -> sem estoque -> descontinuado )

  Diagrama Entidade Relacionamento ( ER )

  <img width="918" height="852" alt="Captura de tela_15-6-2026_134053_www make-charts com" src="https://github.com/user-attachments/assets/dc145f10-dd23-416c-9f5a-c3857614148f" />

  ## Como rodar localmente

- **Pré-requisitos** - Docker e Docker Compose
- ProstregSQL
- Python 3.11

docker-compose up --build

## Lista de Regras de Negócio

-**Produto**
Descrição: Representa um item comercializável no sistema, podendo ser um produto físico ou serviço que possui controle de estoque associado.

| Atributo     | Tipo          | Obrigatório | Constraints                           | Descrição                     |
| :----------- | :------------ | :---------- | :------------------------------------ | :---------------------------- |
| id           | Integer       | Sim         | PK, Auto-incremento                   | Identificador único do produto |
| nome         | String(100)   | Sim         | NOT NULL, UNIQUE, min 1 char          | Nome comercial do produto     |
| descricao    | String(500)   | Não         | -                                     | Descrição detalhada do produto |
| created_at   | DateTime      | Sim         | DEFAULT NOW()                         | Data de criação do registro   |
| updated_at   | DateTime      | Não         | ON UPDATE                             | Data da última alteração      |
| deleted_at   | DateTime      | Não         | NULLABLE                              | Data de soft delete           |

- **Estoque**
Descrição: Controla a quantidade disponível e o estado de um produto específico. Cada produto possui exatamente um registro de estoque.

| Atributo     | Tipo     | Obrigatório | Constraints              | Descrição                                  |
|--------------|----------|-------------|--------------------------|--------------------------------------------|
| id           | Integer  | Sim         | PK, Auto-incremento      | Identificador único do estoque             |
| produto_id   | Integer  | Sim         | FK(produtos.id), UNIQUE  | Referência ao produto                      |
| quantidade   | Integer  | Sim         | DEFAULT 0, >= 0          | Quantidade atual em estoque                |
| status       | Enum     | Sim         | DEFAULT 'ativo'          | Estado atual do estoque                    |
| version      | Integer  | Sim         | DEFAULT 1                | Controle de concorrência otimista          |
| created_at   | DateTime | Sim         | DEFAULT NOW()            | Data de criação                            |
| updated_at   | DateTime | Não         | ON UPDATE                | Data da última atualização                 |

### 
| Campo        | Valor                                                                                                                                                                                                                                                                                         |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Identificador| RN-001                                                                                                                                                                                                                                                                                        |
| Nome         | Integridade de estoque não negativo                                                                                                                                                                                                                                                           |
| Gatilho      | Ao dar baixa, reservar ou atualizar estoque (métodos que diminuem quantidade)                                                                                                                                                                                                                 |
| Pré-condição | Estoque existe e está em estado não terminal (ATIVO, BAIXO, SEM_ESTOQUE ou RESERVADO)                                                                                                                                                                                                          |
| Ação         | Sistema calcula nova_quantidade = quantidade_atual - quantidade_solicitada. Se nova_quantidade < 0, rejeita a operação e retorna erro. Se válida, executa a atualização e registra movimentação.                                                                                             |
| Violação     | HTTP Status: 400 Bad Request<br>Payload:                                                                                                                                                                                                                                                        |
Campo	Valor
Identificador	RN-002
Nome	Controle de concorrência via optimistic locking
Gatilho	Ao atualizar qualquer atributo do estoque (quantidade ou status)
Pré-condição	Cliente fornece a versão atual do registro (obtida na última leitura)
Ação	Sistema verifica se version recebida == version atual no banco. Se igual, atualiza e incrementa version. Se diferente, rejeita com erro de concorrência. Implementa retry com backoff exponencial (3 tentativas).
Violação	HTTP Status: 409 Conflict
Payload:








