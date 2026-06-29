# NLP Portfolio API

NLP Portfolio API é uma plataforma de processamento de linguagem natural construída como serviço REST, projetada para receber texto bruto e devolver análises estruturadas: sentimento, entidades nomeadas, tradução e vetores semânticos. Além das análises pontuais, a API mantém uma memória semântica via ChromaDB (permitindo busca por significado em vez de palavras-chave) e registra o histórico de cada operação em PostgreSQL. O objetivo é demonstrar, na prática, como integrar múltiplos modelos de IA pré-treinados em uma arquitetura modular, conteinerizada e pronta para escalar — servindo tanto como base para aplicações reais (chatbots, classificadores, motores de busca semântica) quanto como portfólio técnico de engenharia de ML.
(Hands-on ML cap 16)
> Pipeline de NLP com FastAPI, HuggingFace e Docker — projeto de portfólio em construção.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![Tests](https://img.shields.io/badge/tests-6%20passed-brightgreen)

---

## Sobre o projeto

API REST para processamento de linguagem natural (NLP) construída com FastAPI e modelos pré-treinados do HuggingFace. O projeto segue um roadmap de 4 fases, evoluindo de um esqueleto básico até um pipeline completo com RAG, orquestração e deploy em produção.

---

## Roadmap

| Fase | Período | Descrição | Status |
|------|---------|-----------|--------|
| 1 | Semanas 1–2 | Setup, FastAPI, Docker, primeiro modelo HF | ✅ Concluída |
| 2 | Semanas 3–4 | Pipeline NLP completo, RAG com ChromaDB, PostgreSQL | ✅ Concluída |
| 3 | Semanas 5–6 | Orquestração n8n, Redis, Slack/Telegram | 🔄 Em andamento |
| 4 | Semanas 7–8 | MLOps, CI/CD, Prometheus, deploy Railway/Fly.io | ⏳ Pendente |

---

## Fase 1 — Setup e base

### O que foi construído

- Estrutura de projeto profissional com separação de responsabilidades
- API REST com FastAPI e documentação Swagger automática
- Containerização completa com Docker e docker-compose
- Integração com modelo HuggingFace de análise de sentimento
- Suite de testes com pytest usando mocks
- Git com conventional commits

### Stack utilizada

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Python | 3.11 | Linguagem base |
| FastAPI | 0.111 | Framework web |
| Uvicorn | 0.29 | Servidor ASGI |
| HuggingFace Transformers | 4.41 | Modelos de NLP |
| PyTorch | 2.3 | Backend dos modelos |
| Pydantic | 2.7 | Validação de dados |
| Docker | — | Containerização |
| pytest | 9.1 | Testes automatizados |

### Modelo integrado

**cardiffnlp/twitter-roberta-base-sentiment-latest**
- Tarefa: classificação de sentimento
- Labels: `positive`, `neutral`, `negative`
- Score: probabilidade de 0 a 1

### Estrutura de pastas

```
nlp-portfolio/
├── app/
│   ├── main.py              # Entrypoint da aplicação
│   ├── config.py            # Configurações via .env
│   ├── routers/
│   │   ├── health.py        # Endpoint de health check
│   │   └── nlp.py           # Endpoints de NLP
│   ├── models/
│   │   └── hf_loader.py     # Carregamento dos modelos HF
│   ├── schemas/
│   │   ├── requests.py      # Modelos de entrada
│   │   └── responses.py     # Modelos de saída
│   └── tests/
│       └── test_api.py      # Testes automatizados
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

### Endpoints disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Informações da API |
| GET | `/health/` | Health check |
| POST | `/nlp/sentiment` | Análise de sentimento |
| GET | `/docs` | Documentação Swagger |

### Exemplo de uso

**Request:**
```bash
curl -X POST http://localhost:8000/nlp/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

**Response:**
```json
{
  "text": "I love this product!",
  "label": "positive",
  "score": 0.9823
}
```

### Testes

```bash
# Rodar os testes dentro do container
docker compose exec api pytest app/tests/ -v
```

Resultado da Fase 1:
```
6 passed in 3.54s
```

---

## Fase 2 — Pipeline NLP completo

### O que foi construído

- 3 novos modelos HuggingFace integrados (NER, Tradução e Embeddings) totalizando **4 modelos** pré-carregados no startup
- **ChromaDB** como banco vetorial embarcado para busca semântica e RAG
- **PostgreSQL** como container separado para histórico persistente de operações
- Camada de serviços (`app/services/`) para isolar lógica de negócio
- Camada de banco de dados (`app/database/`) com SQLAlchemy ORM
- 7 novos endpoints documentados via Swagger
- Volumes Docker persistentes para modelos, ChromaDB e PostgreSQL
- Variáveis de ambiente do HuggingFace (`HF_HOME`) para cache compartilhado

### Stack adicionada

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| sentence-transformers | 2.7 | Geração de embeddings |
| sentencepiece | 0.2 | Tokenização da tradução |
| numpy | 1.23.5 | Fixado para compatibilidade com chroma-hnswlib |
| ChromaDB | 0.5 | Banco vetorial para RAG |
| PostgreSQL | 16-alpine | Banco relacional |
| SQLAlchemy | 2.0 | ORM Python |
| psycopg2-binary | 2.9 | Driver PostgreSQL |

### Modelos integrados nesta fase

| Tarefa | Modelo HuggingFace |
|--------|-------------------|
| NER (entidades nomeadas) | `dbmdz/bert-large-cased-finetuned-conll03-english` |
| Tradução EN→PT | `Helsinki-NLP/opus-mt-tc-big-en-pt` |
| Embeddings (384 dimensões) | `sentence-transformers/all-MiniLM-L6-v2` |

### Arquitetura da Fase 2

```
┌─────────────────────────────────────────┐
│           FastAPI (porta 8000)          │
│  ┌──────────┬──────────┬─────────────┐  │
│  │   NLP    │   RAG    │   History   │  │
│  │ routers  │  router  │   router    │  │
│  └────┬─────┴────┬─────┴──────┬──────┘  │
│       │          │            │         │
│  ┌────▼─────┐ ┌──▼─────┐ ┌────▼─────┐   │
│  │ 4 modelos│ │ Chroma │ │  SQLAlc  │   │
│  │    HF    │ │Service │ │ History  │   │
│  └──────────┘ └────┬───┘ └────┬─────┘   │
└────────────────────┼──────────┼─────────┘
                     │          │
              ┌──────▼─────┐ ┌──▼─────────┐
              │ ChromaDB   │ │ PostgreSQL │
              │ (embarcado)│ │ container  │
              └────────────┘ └────────────┘
```

### Estrutura de pastas atualizada

```
nlp-portfolio/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   │   ├── health.py
│   │   ├── nlp.py             # 4 endpoints NLP com histórico
│   │   ├── rag.py             # NOVO: documentos e busca
│   │   └── history.py         # NOVO: listagem de histórico
│   ├── models/
│   │   └── hf_loader.py       # 4 modelos carregados no startup
│   ├── schemas/
│   │   ├── requests.py
│   │   └── responses.py
│   ├── services/              # NOVO
│   │   ├── chroma_service.py  # Lógica do ChromaDB
│   │   └── history_service.py # Lógica do histórico
│   ├── database/              # NOVO
│   │   ├── connection.py      # Engine e session SQLAlchemy
│   │   └── models.py          # Tabela NLPHistory
│   └── tests/
├── chroma_data/               # Volume persistente do ChromaDB
├── postgres_data/             # Volume persistente do PostgreSQL
└── docker-compose.yml         # Agora com 2 serviços: api + postgres
```

### Endpoints da Fase 2

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/nlp/sentiment` | Análise de sentimento (com histórico) |
| POST | `/nlp/ner` | Reconhecimento de entidades nomeadas |
| POST | `/nlp/translate` | Tradução EN→PT |
| POST | `/nlp/embeddings` | Geração de vetor semântico (384 dim) |
| POST | `/rag/documents` | Adiciona documento ao banco vetorial |
| POST | `/rag/search` | Busca semântica por similaridade |
| GET | `/rag/stats` | Total de documentos indexados |
| GET | `/history/` | Histórico de operações (filtrável) |

### Exemplos de uso

**NER:**
```bash
curl -X POST http://localhost:8000/nlp/ner \
  -H "Content-Type: application/json" \
  -d '{"text": "Aline works at Google in São Paulo."}'
```
```json
{
  "text": "Aline works at Google in São Paulo.",
  "entities": [
    {"word": "Aline", "entity": "PER", "score": 0.9987, "start": 0, "end": 5},
    {"word": "Google", "entity": "ORG", "score": 0.9991, "start": 15, "end": 21},
    {"word": "São Paulo", "entity": "LOC", "score": 0.9978, "start": 25, "end": 34}
  ]
}
```

**Tradução EN→PT:**
```bash
curl -X POST http://localhost:8000/nlp/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you today?", "source": "en"}'
```
```json
{
  "original": "Hello, how are you today?",
  "translated": "Olá, como você está hoje?",
  "source": "en",
  "target": "pt"
}
```

**Busca semântica (RAG):**
```bash
# Primeiro, adicionar documentos
curl -X POST http://localhost:8000/rag/documents \
  -H "Content-Type: application/json" \
  -d '{"text": "FastAPI é um framework Python moderno e rápido.", "metadata": {"tema": "tecnologia"}}'

# Depois, buscar por significado (não por palavras)
curl -X POST http://localhost:8000/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query": "linguagem de programação", "top_k": 2}'
```

A busca retorna documentos por **proximidade semântica**, mesmo sem palavras em comum com a query.

**Histórico:**
```bash
# Todas as operações
curl http://localhost:8000/history/?limit=10

# Filtrar por tipo
curl "http://localhost:8000/history/?operation=sentiment&limit=5"
```

### Variáveis de ambiente adicionadas

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `HF_MODEL_NER` | `dbmdz/bert-large-cased-finetuned-conll03-english` | Modelo NER |
| `HF_MODEL_TRANSLATION` | `Helsinki-NLP/opus-mt-tc-big-en-pt` | Modelo tradução |
| `HF_MODEL_EMBEDDINGS` | `sentence-transformers/all-MiniLM-L6-v2` | Modelo embeddings |
| `DATABASE_URL` | `postgresql://nlp_user:nlp_pass@postgres:5432/nlp_db` | URL do PostgreSQL |
| `HF_HOME` | `/app/models` | Cache compartilhado HuggingFace |

### Notas técnicas

- **Persistência:** ChromaDB e PostgreSQL têm volumes mapeados (`./chroma_data` e `./postgres_data`), preservando dados entre reinícios dos containers
- **Conflito de porta:** se houver outro PostgreSQL na porta 5432, o `docker-compose.yml` mapeia o nosso para `5433:5432` externamente; a comunicação interna entre containers continua via porta 5432
- **Cache de modelos:** a primeira execução baixa ~2GB de modelos do HuggingFace; execuções subsequentes usam o cache local em `./models`
- **Telemetria do ChromaDB:** os warnings `posthog telemetry` no startup são inofensivos e podem ser ignorados

---

## Como rodar localmente

### Pré-requisitos

- Docker
- Docker Compose

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/nlp-portfolio.git
cd nlp-portfolio

# 2. Copie o arquivo de variáveis de ambiente
cp .env.example .env

# 3. Suba os containers
docker compose up --build

# 4. Acesse a documentação
# http://localhost:8000/docs
```

---

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `APP_ENV` | `development` | Ambiente da aplicação |
| `APP_VERSION` | `0.1.0` | Versão da API |
| `HF_CACHE_DIR` | `./models` | Diretório de cache dos modelos |
| `HF_MODEL_SENTIMENT` | `cardiffnlp/twitter-roberta-base-sentiment-latest` | Modelo de sentimento |
| `HF_MODEL_NER` | `dbmdz/bert-large-cased-finetuned-conll03-english` | Modelo NER |
| `HF_MODEL_TRANSLATION` | `Helsinki-NLP/opus-mt-tc-big-en-pt` | Modelo tradução |
| `HF_MODEL_EMBEDDINGS` | `sentence-transformers/all-MiniLM-L6-v2` | Modelo embeddings |
| `DATABASE_URL` | `postgresql://nlp_user:nlp_pass@postgres:5432/nlp_db` | Conexão PostgreSQL |

---

## Licença

MIT