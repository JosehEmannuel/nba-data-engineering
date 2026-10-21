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

- `src/ingestion/`: pipelines de carga de times, jogadores, jogos e estatísticas.
- `src/repositories/`: acesso às tabelas por repositórios e Unit of Work.
- `src/transform/`: atualização da camada analítica dimensional.
- `sql/`: schema de ingestão, star schema, índices e views.
- `tests/`: testes automatizados.

## Como executar

1. Instale as dependências com `pip install -r requirements.txt`.
2. Copie `.env.example` para `.env` e informe as credenciais do MySQL.
3. Crie as tabelas sem remover dados existentes: `python -m src.database.initialize`.
4. Carregue times e jogadores:
   `python -m src.ingestion.load_teams` e `python -m src.ingestion.load_players`.
5. Enriqueça os jogadores: `python -m src.ingestion.enrich_players`.
   O pipeline confirma cada lote de 25 jogadores; se a API falhar, os jogadores
   sem checkpoint podem ser tentados na próxima execução.
6. Configure `NBA_START_SEASON` e `NBA_END_SEASON` no `.env` e carregue os jogos
   da temporada regular com `python -m src.ingestion.load_games`. O padrão cobre
   de 1946-47 a 2025-26; o endpoint usado disponibiliza partidas a partir de
   1983-84 e registra temporadas anteriores como consultadas sem jogos.
7. Carregue os playoffs com `python -m src.ingestion.load_playoffs`.
8. Carregue estatísticas individuais por partida com
   `python -m src.ingestion.load_player_game_stats`. Esta etapa consulta jogo a
   jogo, pode levar várias horas e é retomável por jogo.
9. Atualize as dimensões e fatos do Power BI com
   `python -m src.transform.build_star_schema`.

Os IDs de times de jogadores históricos são preservados mesmo quando a franquia
não está na dimensão atual. Os campos de texto da NBA API também podem variar
historicamente, por exemplo em números de camisa compostos.

## Roadmap

- [x] Modelagem da tabela Players
- [x] Pipeline de ingestão de jogadores
- [x] Pipeline de Times
- [x] Pipeline de Jogos históricos por temporada
- [x] Pipeline de playoffs
- [x] Estatísticas dos jogadores por partida
- [x] Modelagem Star Schema
- [ ] Dashboard Power BI
- [ ] Docker
- [ ] Airflow

## Camada analítica

Execute `python -m src.transform.build_star_schema` depois das cargas para
atualizar as dimensões e fatos do Power BI. O guia de conexão e medidas iniciais
está em [docs/powerbi.md](docs/powerbi.md).
