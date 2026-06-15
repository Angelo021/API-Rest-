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

### Estoque não pode ficar negativo
| Campo        | Valor                                                                                                                                                                                                                                                                                         |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Identificador| RN-001                                                                                                                                                                                                                                                                                        |
| Nome         | Integridade de estoque não negativo                                                                                                                                                                                                                                                           |
| Gatilho      | Ao dar baixa, reservar ou atualizar estoque (métodos que diminuem quantidade)                                                                                                                                                                                                                 |
| Pré-condição | Estoque existe e está em estado não terminal (ATIVO, BAIXO, SEM_ESTOQUE ou RESERVADO)                                                                                                                                                                                                          |
| Ação         | Sistema calcula nova_quantidade = quantidade_atual - quantidade_solicitada. Se nova_quantidade < 0, rejeita a operação e retorna erro. Se válida, executa a atualização e registra movimentação.                                                                                             |
| Violação     | HTTP Status: 400 Bad Request<br>Payload:                                                                                                                                                                                                                                                        |

###Versionamento 
<img width="993" height="1404" alt="image" src="https://github.com/user-attachments/assets/064873bd-259a-4749-9ff4-5f96ae4a7ef3" />










