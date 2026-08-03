# 🏀 NBA Data Engineering Pipeline

Projeto desenvolvido para praticar Engenharia de Dados utilizando dados reais da NBA.

## Objetivos

- Construção de pipelines ETL
- Modelagem de banco de dados
- Consumo de APIs
- Tratamento e transformação de dados
- Persistência em MySQL
- Arquitetura organizada para projetos de dados

## Tecnologias

- Python
- Pandas
- MySQL
- NBA API
- Git
- GitHub

## Estrutura

src/
database/
ingestion/
transform/

sql/
├── schema.sql
├── indexes.sql
└── views.sql

## Como executar

1. Copie `.env.example` para `.env` e informe as credenciais do MySQL.
2. Crie as tabelas sem remover dados existentes: `python -m src.database.initialize`.
3. Carregue as dimensões: `python -m src.ingestion.load_teams` e `python -m src.ingestion.load_players`.
4. Enriqueça os jogadores: `python -m src.ingestion.enrich_players`.
5. Carregue jogos históricos: defina `NBA_START_SEASON` e `NBA_END_SEASON` no
   `.env` e execute `python -m src.ingestion.load_games`. O padrão cobre de
   1946-47 a 2025-26, somente jogos de temporada regular. Atualmente, o
   endpoint utilizado pela NBA API disponibiliza partidas a partir de 1983-84;
   as temporadas anteriores ficam registradas como consultadas sem jogos.
6. Carregue os playoffs com `python -m src.ingestion.load_playoffs`.
7. Carregue estatísticas individuais por partida com
   `python -m src.ingestion.load_player_game_stats`. Esta etapa faz uma consulta
   por jogo e pode levar várias horas; ela é retomável por jogo e utiliza o
   endpoint V3 da NBA API, com fallback para V2 em partidas históricas.

O enriquecimento confirma cada lote de 25 jogadores. Se a API falhar, apenas os
jogadores sem checkpoint serão tentados na próxima execução.

Os IDs de time de jogadores históricos são preservados mesmo quando a franquia
não está na dimensão atual de times.

Os campos de texto oriundos da NBA API comportam variações históricas, como
números de camisa compostos.

## Roadmap

- [x] Modelagem da tabela Players
- [x] Pipeline de ingestão de jogadores
- [x] Pipeline de Times
- [x] Pipeline de Jogos históricos por temporada
- [x] Pipeline de playoffs
- [x] Estatísticas dos jogadores por partida
- [ ] Modelagem Star Schema
- [ ] Dashboard
- [ ] Docker
- [ ] Airflow
